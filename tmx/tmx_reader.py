#!/usr/bin/env python
import argparse
import sys
import xml.etree.ElementTree as ET


def find_segment(tag):
    for n in range(len(tag)):
        if tag[n].tag == 'seg':
            return n
    sys.stderr.write('Error: segment not found.\n')
    sys.exit(-1)


def find_body(root):
    for n in range(len(root)):
        if root[n].tag == 'body':
            return n
    sys.stderr.write('Error parsing tmx.\n')
    sys.exit(-1)


def parse_args():
    parser = argparse.ArgumentParser(description='This script extracts \
                                     source and target sentences from \
                                     a tmx file.')
    parser.add_argument('-f', '--file', metavar='file', required=True,
                        help='tmx file from which to extract the sentences.')
    parser.add_argument('-s', '--source', metavar='src_language',
                        required=True, help='source language.')
    parser.add_argument('-t', '--target', metavar='tgt_language',
                        required=True, help='target language.')
    parser.add_argument('-n', '--name', metavar='files_name', required=True,
                        help='name to use for creating the output files. \
                        files_name.src will contain the source sentences and \
                        files_name.tgt the target sentences.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    try:
        tree = ET.parse(args.file)
    except IOError:
        sys.stderr.write('Error: ' + args.file + ' does not exist.\n')
        sys.exit(-1)
    except SyntaxError:
        sys.stderr.write('Error: ' + args.file + ' is not a tmx file.\n')
        sys.exit(-1)

    src = open(args.name + '.src', 'w')
    tgt = open(args.name + '.tgt', 'w')
    root = tree.getroot()
    body = root[find_body(root)]
    for segment in body:
        for tag in segment:
            if tag.tag == 'tuv':
                if args.source in tag.attrib.values():
                    src.write(tag[find_segment(tag)].text + '\n')
                elif args.target in tag.attrib.values():
                    tgt.write(tag[find_segment(tag)].text + '\n')
    src.close()
    tgt.close()
