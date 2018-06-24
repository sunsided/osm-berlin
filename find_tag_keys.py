import os

from collections import Counter
from tqdm import tqdm
from argparse import ArgumentParser

from data_wrangling.xml_processing.parsing import open_and_parse


parser = ArgumentParser()
parser.add_argument('file', nargs='?',
                    default=os.path.join('osm-extracts', 'berlin.osm.bz2'),
                    help='The OSM map file to scan.')
args = parser.parse_args()

if not os.path.exists(args.file) or not os.path.isfile(args.file):
    parser.error(f'The specified argument is not a valid file: {args.file}')
    exit(1)

cnt = Counter()
progress = tqdm()

for ev, el in open_and_parse(args.file, events=('start',), progress=progress):
    if el.tag == 'osm':
        assert 'version' in el.attrib and el.attrib['version'] == '0.6', 'Unknown version of the OSM format.'
    tag_keys = [tag.attrib['k'] for tag in el.iter('tag')]
    cnt.update(tag_keys)


progress.close()

print('Tag key counts:')
for key, count in sorted(cnt.items(), key=lambda x: x[0]):
    print(f'{count:10d} {key:s}')
