#!/usr/bin/env python

import matplotlib.pyplot as plt
import argparse
import numpy as np
import os


def parse_args():
    parser = argparse.ArgumentParser(description='This script generates\
                                     a histogram of the number of words per\
                                     sentence in a given document.')
    parser.add_argument('-f', '--files', metavar='files', nargs='+',
                        required=True, help='document to analyze.')
    parser.add_argument('-o', '--output', metavar='image',
                        required=True, help='image containing the instagram.')
    parser.add_argument('-t', '--title', metavar='title', required=True,
                        help='title for the histogram.')
    parser.add_argument('-l', '--lower', metavar='lower', default=-1,
                        type=float, help='lower interval, around the mean, in \
                        which to center the histogram.: lower * mean. \
                        (Default: no limit.)')
    parser.add_argument('-u', '--upper', metavar='upper', default=-1,
                        type=float, help='upper interval, around the mean, in \
                        which to center the histogram.: upper * mean. \
                        (Default: no limit.)')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    words = []
    labels = []
    d = {}
    for f in args.files:
        words.append(np.array([len(line.split()) for line in open(f)]))
        labels.append(os.path.basename(f))
    plt.hist(words, bins='auto', alpha=0.5, label=labels)
    min_ylim, max_ylim = plt.ylim()
    if args.lower >= 0 and args.upper >= 0:
        plt.xlim(min([args.lower * w.mean() for w in words]),
                 max([args.upper * w.mean() for w in words]))
    plt.legend()
    plt.xlabel('Words per sentence')
    plt.ylabel('Nº of sentences')
    plt.title(args.title)
    plt.savefig(args.output)
