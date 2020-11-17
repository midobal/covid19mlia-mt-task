#!/usr/bin/env python
import argparse
import sys
import os
import lxml.etree as ET


def parse_args():
    parser = argparse.ArgumentParser(description='This script extracts\
                                     segments from a sgm file.')
    parser.add_argument('-f', '--file', metavar='sgm_file',
                        required=True, help='sgm file from which to extract\
                        the segments.')
    parser.add_argument('-o', '--output', metavar='output_file',
                        help='file in which to store the segment. \
                        (Default: create documents using the \
                        docid from the sgm.)')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    try:
        tree = ET.parse(args.file,  ET.XMLParser(recover=True))
    except IOError:
        sys.stderr.write('Error: ' + args.file + ' does not exist.\n')
        sys.exit(-1)
    except SyntaxError:
        sys.stderr.write('Error parsing ' + args.file + '.\n')
        sys.exit(-1)

    root = tree.getroot()
    if args.output is not None:
        output = open(args.output, 'w')
    for document in root:
        if args.output is None:
            output = open(document.attrib['docid'].replace('/', '_'), 'w')
        for tag in document:
            if tag.tag == 'hl' or tag.tag == 'p':
                for seg in tag:
                    if seg.text is None:
                        output.write('\n')
                    else:
                        output.write(seg.text.strip() + '\n')
            elif tag.tag == 'seg':
                if tag.text is None:
                    output.write('\n')
                else:
                    output.write(tag.text.strip() + '\n')
        if args.output is None:
            output.close()
    if args.output is not None:
        output.close()
