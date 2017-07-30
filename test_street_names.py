import os

from argparse import ArgumentParser

from auditing.streets import audit_street_name


def main():
    parser = ArgumentParser()
    parser.add_argument('file', default='street_names.txt', nargs='?', help='The street name file to use.')
    args = parser.parse_args()

    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        parser.error(f'The specified argument is not a valid file: {args.file}')
        exit(1)

    with open(args.file, 'r', encoding='utf-8') as f:
        for line in f:
            name = line.rstrip(os.linesep)
            was_valid, valid = audit_street_name(name)
            if valid is None:
                print(f'Skipped "{name}": Not a street.')
                continue

            if not was_valid:
                print(f'Corrected "{name}" to "{valid}".')


if __name__ == '__main__':
    main()
