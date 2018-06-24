"""
This script extracts street names from an OpenStreetMap XML file
and writes them to a separate text file.
"""

import os
from argparse import ArgumentParser

from tqdm import tqdm

from data_wrangling.xml_processing import open_and_parse


def is_street_name(elem):
    assert 'k' in elem.attrib and 'v' in elem.attrib
    return elem.attrib['k'] == 'addr:street'


def validate_osm_version(events):
    ev, el = next(events)
    assert el.tag == 'osm'
    assert 'version' in el.attrib and el.attrib['version'] == '0.6', 'Unknown version of the OSM format.'


def main():
    parser = ArgumentParser()
    parser.add_argument('file', nargs='?',
                        default=os.path.join('osm-extracts', 'berlin.osm.bz2'),
                        help='The OSM map file to scan.')
    parser.add_argument('--out', type=str,
                        default='street_names.txt',
                        help='The file to write street names to.')
    args = parser.parse_args()

    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        parser.error(f'The specified argument is not a valid file: {args.file}')
        exit(1)

    progress = tqdm()

    events = open_and_parse(args.file, events=('start',), progress=progress)
    validate_osm_version(events)

    street_names = set()
    for ev, el in events:
        assert el.tag != 'osm'
        if el.tag == 'way':
            street_name_tags = (tag for tag in el.iter('tag') if is_street_name(tag))
            for tag in street_name_tags:
                street_names.add(tag.attrib['v'])

    with open(args.out, 'w', encoding='utf-8') as f:
        first = True
        for s in sorted(street_names):
            if not first:
                f.write('\n')
            first = False
            f.write(s)


if __name__ == '__main__':
    main()
