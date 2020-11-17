#!/usr/bin/env python
import argparse
import sys
import os
import lxml.etree as ET


def generate_document(file, root):
    try:
        f = open(file, 'r')
    except IOError:
        sys.stderr.write('Error: ' + file + ' does not exist.\n')
        sys.exit(-1)

    document = ET.SubElement(root, 'doc', docid=os.path.basename(file))
    counter = 1
    for seg in f.readlines():
        segment = ET.SubElement(document, 'seg', id=str(counter))
        segment.text = seg.strip()
        counter += 1


def parse_args():
    parser = argparse.ArgumentParser(description='This script generates\
                                     an sgm file.')
    parser.add_argument('-f', '--files', metavar='text_files', nargs='+',
                        required=True, help='text files to convert into sgm.')
    parser.add_argument('-o', '--output', metavar='sgm_file',
                        required=True, help='file in which to store the sgm.')
    parser.add_argument('-i', '--id', metavar='id', help='id to include in \
                        the file. (Default: test.)')
    parser.add_argument('-r', '--reference', default=False,
                        action='store_true', help='indicates that the file \
                        is intented to be used as a reference.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    type = 'srcset' if not args.reference else 'refset'
    id = args.id if args.id is not None else 'test'

    root = ET.Element(type, setid=id, srclang='any')
    for file in args.files:
        generate_document(file, root)
    output = open(args.output, 'w')
    output.write(ET.tostring(root, pretty_print=True,
                             encoding='utf8').decode('utf8'))
    output.close()
