import os
import re

from argparse import ArgumentParser
from pprint import pprint
from typing import Tuple, Optional, Callable

from tqdm import tqdm
from xml.etree.cElementTree import Element

from pymongo import MongoClient
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

    #client = MongoClient(args.connection)
    #database = client.get_default_database()
    #collection = database.get_collection('osm_berlin')

    progress = tqdm()

    events = open_and_parse(args.file, events=('start',), progress=progress)
    validate_osm_version(events)

    for ev, el in events:
        assert el.tag != 'osm'

        for audit in auto_audit:
            el = audit(el)
            if el is not None:
                continue

    progress.close()
    print('Audit summary:')
    for audit in auto_audit:
        print('- ' + str(audit))


if __name__ == '__main__':
    main()
