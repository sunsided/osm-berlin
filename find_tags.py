import os

from collections import Counter
from tqdm import tqdm
from argparse import ArgumentParser

from xml_processing.parsing import open_and_parse


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
stack = []

for ev, el in open_and_parse(args.file, events=('start', 'end'), progress=progress):
    if ev == 'start':
        if el.tag == 'osm':
            assert 'version' in el.attrib and el.attrib['version'] == '0.6', 'Unknown version of the OSM format.'
        stack.append(el.tag)
        path = '.'.join(stack)
        cnt[path] += 1
    else:
        stack.pop()
        

progress.close()

print('XML item counts:')
for item in sorted(cnt.items(), key=lambda x: len(x[0])):
    print(f'{item[1]:10d} {item[0]:s}')
