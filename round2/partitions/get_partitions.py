#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import random
import os
import sys


class Segment:
    def __init__(self, score, src, tgt, origin):
        self.score = score
        self.src = src
        self.tgt = tgt
        self.origin = origin

    def get_length(self):
        return len(self.src.split())

    def get_origin(self):
        return self.origin

    def get_source(self):
        return self.src

    def get_target(self):
        return self.tgt

    def get_escaped_source(self):
        return (self.src.replace('<', '&lt;').replace('&', '&amp;').
                replace('>', '&gt;').replace('"', '&quot;').
                replace("'", '&apos;'))

    def get_escaped_target(self):
        return (self.tgt.replace('<', '&lt;').replace('&', '&amp;').
                replace('>', '&gt;').replace('"', '&quot;').
                replace("'", '&apos;'))

    def __repr__(self):
        return repr((self.score, self.src, self.tgt, self.origin))


def generate_tmx(data, src, tgt, file):
    f = open(file, 'w')
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<tmx version="1.4">\n')
    f.write('   <!--Simplified custom tmx version.-->\n')
    f.write('   <body>\n')

    for n in range(len(data)):
        # New segment
        f.write('      <tu tuid="' + str(n + 1) + '">\n')

        # Source
        f.write('         <tuv xml:lang="' + src + '">\n')
        f.write('            <seg>' + data[n].get_escaped_source()
                + '</seg>\n')
        f.write('         </tuv>\n')

        # Target
        f.write('         <tuv xml:lang="' + tgt + '">\n')
        f.write('            <seg>' + data[n].get_escaped_target()
                + '</seg>\n')
        f.write('         </tuv>\n')

        f.write('      </tu>\n')

    f.write('   </body>\n')
    f.write('</tmx>\n')
    f.close()


def parse_args():
    parser = argparse.ArgumentParser(description='This script generates\
                                     train, dev and test partitions (in tmx) \
                                     from a set of tsv files.')
    parser.add_argument('-f', '--files', metavar='files', nargs='+',
                        required=True, help='tsv files containing the data.')
    parser.add_argument('-l', '--lower', metavar='lower', default=0.7,
                        type=float, help='lower interval for selecting dev \
                        and test: lower * mean. (Default: 0.7.)')
    parser.add_argument('-u', '--upper', metavar='upper', default=1.3,
                        type=float, help='upper interval for selecting dev \
                        and test: upper * mean. (Default: 1.3.)')
    parser.add_argument('-w', '--max_words', metavar='max_words', default=0,
                        type=int, help='maximum number of words per segment. \
                        (Default: no limit.)')
    parser.add_argument('-n', '--n_segments', metavar='n_segments', type=int,
                        default=4000, help='maximum number of words per \
                        segment. (Default: no limit.)')
    parser.add_argument('-s', '--src', metavar='source_language',
                        required=True, help='source language.')
    parser.add_argument('-t', '--tgt', metavar='target_language',
                        required=True, help='target language.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    segments = []
    means = {}
    total_segments = []
    src_counts = {}

    # Read data
    for f in args.files:
        if not os.path.isfile(f):
            sys.stderr.write('Error: file ' + f + ' does not exist.\n')
            sys.exit(-1)
        n_segments = 0
        src_length = 0
        for l in open(f):
            segment = l.strip().split('\t')
            if args.max_words == 0 or (len(segment[1].split())
                                       <= args.max_words
                                       and len(segment[2].split())
                                       <= args.max_words):
                segments.append(Segment(float(segment[0]), segment[1],
                                        segment[2], f))
                n_segments += 1
                src_length += len(segment[1].split())
                try:
                    src_counts[segment[1]] += 1
                except KeyError:
                    src_counts[segment[1]] = 1
        means[f] = float(src_length / n_segments)
        total_segments.append(n_segments)
    # Sort data by score
    sorted_segments = sorted(segments, key=lambda segment: segment.score)[::-1]

    # Add dev and test to a pool, and the rest for training
    pool = []
    train = []
    remaining = {}
    for n in range(len(total_segments)):
        remaining[args.files[n]] = round(total_segments[n] * args.n_segments
                                         * 2 / len(segments))
    for segment in segments:
        segment_length = segment.get_length()
        origin = segment.get_origin()
        lower_limit = args.lower * means[origin]
        upper_limit = args.upper * means[origin]
        if (remaining[origin] > 0 and src_counts[segment.get_source()] == 1
                and segment_length >= lower_limit
                and segment_length <= upper_limit):
            pool.append(segment)
            remaining[origin] -= 1
        else:
            train.append(segment)

    # Shuffle pool and split equally into dev and test
    dev = []
    test = []
    random.shuffle(pool)
    for n in range(len(total_segments)):
        remaining[args.files[n]] = round(total_segments[n]
                                         / float(len(segments))
                                         * args.n_segments)

    for segment in pool:
        origin = segment.get_origin()
        if remaining[origin] > 0:
            dev.append(segment)
            remaining[origin] -= 1
        else:
            test.append(segment)

    # Generate tmx files
    generate_tmx(dev, args.src, args.tgt, args.src + args.tgt + '-dev.tmx')
    generate_tmx(test, args.src, args.tgt, args.src + args.tgt + '-test.tmx')
    max_sements = 100000
    if len(train) < max_sements:  # Split train file if it's too big.
        generate_tmx(train, args.src, args.tgt, args.src + args.tgt
                     + '-tr.tmx')
    else:
        counter = 0
        for n in range(max_sements, len(train), max_sements):
            generate_tmx(train[n - max_sements:n], args.src, args.tgt, args.src
                         + args.tgt + '-tr' + str(counter) + '.tmx')
            counter += 1
        generate_tmx(train[len(train) // max_sements * max_sements:], args.src,
                     args.tgt, args.src + args.tgt + '-tr' + str(counter)
                     + '.tmx')
