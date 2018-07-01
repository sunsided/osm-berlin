import os
from datetime import datetime

from argparse import ArgumentParser
from typing import Dict, Tuple

import bson
from tqdm import tqdm
from xml.etree.cElementTree import Element
import pymongo
from data_wrangling.xml_processing import open_and_parse
from data_wrangling.auditing import AuditStreetName


def validate_osm_version(events):
    ev, el = next(events)
    assert el.tag == 'osm'
    assert 'version' in el.attrib and el.attrib['version'] == '0.6', 'Unknown version of the OSM format.'


auto_audit = [
    AuditStreetName()
]


def main():
    parser = ArgumentParser()
    parser.add_argument('file', nargs='?',
                        default=os.path.join('osm-extracts', 'berlin.osm.bz2'),
                        help='The OSM map file to scan.')
    parser.add_argument('--connection', default='mongodb://localhost:27017/dand',
                        help='The MongoDB connection string.')
    args = parser.parse_args()

    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        parser.error(f'The specified argument is not a valid file: {args.file}')
        exit(1)

    client = pymongo.MongoClient(args.connection)
    database = client.get_default_database()
    collection = database.get_collection('osm_berlin')

    collection.create_index([('_id.type', pymongo.ASCENDING)], background=True, unique=False)
    collection.create_index([('user.name', pymongo.ASCENDING)], background=True, unique=False)
    collection.create_index([('user.id', pymongo.ASCENDING)], background=True, unique=False)
    collection.create_index([('t', pymongo.ASCENDING)], background=True, unique=False)
    collection.create_index([('tag_keys', pymongo.TEXT),
                             ('tag_values', pymongo.TEXT)], background=True, unique=False)
    collection.create_index([('loc', pymongo.GEOSPHERE)],
                            background=True, unique=False,
                            partialFilterExpression={'_id.type': 'node'})

    progress = tqdm()

    events = open_and_parse(args.file, events=('start',), progress=progress)
    validate_osm_version(events)

    for ev, el in events:
        assert el.tag != 'osm'
        if el.tag != 'node' and el.tag != 'way' and el.tag != 'relation':
            continue

        for audit in auto_audit:
            el = audit(el)
            if el is not None:
                continue

        id, doc = elem_to_doc(el)

        find = {'_id': id}
        update = {'$set': doc}
        collection.update(find, update, upsert=True)

    progress.close()
    print('Audit summary:')
    for audit in auto_audit:
        print('- ' + str(audit))


def parse_date(inp: str) -> datetime:
    # 2015-11-15T09:51:47Z
    return datetime.strptime(inp, '%Y-%m-%dT%H:%M:%SZ')


def elem_to_doc(el: Element) -> Tuple[Dict, Dict]:
    id = {
            'type': el.tag,
            'id': bson.Int64(el.attrib['id'])
        }

    time = parse_date(el.attrib['timestamp'])
    user = {
                'name': el.attrib['user'],
                'id': el.attrib['uid']
            }

    doc = {}
    if el.tag == 'node':
        doc = {
            't': time,
            'user': user,
            'loc': {
                'type': 'Point',
                'coordinates': [
                    float(el.attrib['lon']),
                    float(el.attrib['lat'])
                ]
            }
        }
    elif el.tag == 'way':
        doc = {
            't': time,
            'user': user,
            'nodes': [bson.Int64(x.attrib['ref']) for x in el.iter('nd')]
        }
    elif el.tag == 'relation':
        doc = {
            't': time,
            'user': user,
            'members': [
                {
                    'type': x.attrib['type'],
                    'ref': bson.Int64(x.attrib['ref']),
                    'role': x.attrib['role']
                }
                for x in el.iter('member')
            ]
        }

    tags = {}
    for tag in el.iter('tag'):
        key = tag.attrib['k']
        value = tag.attrib['v']
        tags[key] = value

    if len(tags) > 0:
        doc['tags'] = tags
        doc['tag_keys'] = list(tags.keys())
        doc['tag_values'] = '\n'.join(list(tags.values()))

    return id, doc


if __name__ == '__main__':
    main()
