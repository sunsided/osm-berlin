import os

from collections import Counter
from tqdm import tqdm
from argparse import ArgumentParser

from xml_processing.parsing import open_and_parse


parser = ArgumentParser()
parser.add_argument('file', default='berlin_germany.osm.bz2', nargs='?', help='The OSM map file to scan.')
args = parser.parse_args()

if not os.path.exists(args.file) or not os.path.isfile(args.file):
    parser.error(f'The specified argument is not a valid file: {args.file}')
    exit(1)

cnt = Counter()
progress = tqdm()
stack = []

for event in open_and_parse(args.file, events=('start', 'end'), progress=progress):
    ev, tag = event[0], event[1].tag
    if ev == 'start':
        stack.append(tag)
        path = '.'.join(stack)
        cnt[path] += 1
    else:
        stack.pop()

progress.close()

print('XML item counts:')
for item in sorted(cnt.items(), key=lambda x: len(x[0])):
    print(f'{item[1]:10d} {item[0]:s}')
