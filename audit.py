import os
import re

from argparse import ArgumentParser
from pprint import pprint
from typing import Set

from tqdm import tqdm

from xml_processing.parsing import open_and_parse


def is_street_name(elem):
    assert 'k' in elem.attrib and 'v' in elem.attrib
    return elem.attrib['k'] == 'addr:street'


# street_types_re = re.compile(r'(\b(allee)|(str\.?|stra(ß|ss)e|weg|platz))$', re.IGNORECASE)
street_types_re = re.compile(r'(\b(allee)|([^\b]|er\s)(straße|weg|platz))$', re.IGNORECASE)


def audit_street_type(street_names: Set[str], street_name: str):
    m = street_types_re.search(street_name)
    if not m:
        street_names.add(street_name)


def collect_street_type(street_names: Set[str], street_name: str):
    m = street_types_re.search(street_name)
    if not m:
        street_names.add(street_name)


def validate_osm_version(events):
    ev, el = next(events)
    assert el.tag == 'osm'
    assert 'version' in el.attrib and el.attrib['version'] == '0.6', 'Unknown version of the OSM format.'


def main():
    parser = ArgumentParser()
    parser.add_argument('file', nargs='?',
                        default=os.path.join('osm-extracts', 'berlin.osm.bz2'),
                        help='The OSM map file to scan.')
    args = parser.parse_args()

    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        parser.error(f'The specified argument is not a valid file: {args.file}')
        exit(1)

    progress = tqdm()

    events = open_and_parse(args.file, events=('start',), progress=progress)
    validate_osm_version(events)

    invalid_street_names = set()
    for ev, el in events:
        assert el.tag != 'osm'
        if el.tag == 'way':
            street_name_tags = (tag for tag in el.iter('tag') if is_street_name(tag))
            for tag in street_name_tags:
                audit_street_type(invalid_street_names, tag.attrib['v'])

    pprint(invalid_street_names)


if __name__ == '__main__':
    main()
