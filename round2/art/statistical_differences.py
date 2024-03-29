#!/usr/bin/env python
import argparse
import sys
import lxml.etree as ET
import sacrebleu
from art import aggregators
from art import scores
from art import significance_tests
import os
import time
import subprocess


def save_to_file(sentence):
    file = '/tmp/' + str(time.time()) + '_covid19mlia'
    with open(file, 'w') as f:
        f.write(sentence)
    return file


def assess_differences(a_metrics, b_metrics, trials, p_value):
    test = significance_tests.ApproximateRandomizationTest(
        scores.Scores([scores.Score(m) for m in a_metrics]),
        scores.Scores([scores.Score(m) for m in b_metrics]),
        aggregators.average,
        trials=trials)

    if test.run() < p_value:
        print('Systems are statistically different.')
    else:
        print('Systems are not statistically different.')


def compute_metrics(ref, hyp, hyp_order, metric):
    # Read sentences
    refs = []
    hyps = []
    for id in hyp_order:
        for segment in hyp[id]:
            hyps.append(segment)
        try:
            for segment in ref[id]:
                refs.append(segment)
        except KeyError:
            sys.stderr.write('Error: there are no references for document'
                             + ' "' + id + '"\n')
            sys.exit(-1)

    scores = []
    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    for n in range(len(hyps)):
        if metric == 'bleu':
            try:
                score = sacrebleu.corpus_bleu([hyps[n]], [[refs[n]]])
            except EOFError:
                sys.stderr.write('Error: source and reference have different'
                                 + ' lengths.\n')
                sys.exit(-1)

        elif metric == 'ter':
            try:
                score = sacrebleu.corpus_ter([hyps[n]], [[refs[n]]])
            except EOFError:
                sys.stderr.write('Error: source and reference have different'
                                 + ' lengths.\n')
                sys.exit(-1)

        else:
            hyps_file = save_to_file(hyps[n])
            refs_file = save_to_file(refs[n])
            try:
                process = subprocess.Popen((dir + '/beer_2.0/beer -s '
                                            + hyps_file + ' -r '
                                            + refs_file).split(),
                                           stdout=subprocess.PIPE)
                score, error = process.communicate()
            except FileNotFoundError:
                sys.stderr.write('Error: Beer requirement has not been'
                                 + 'satisfied.\n')
                sys.exit(-1)

            # Delete aux files
            process = subprocess.Popen(('rm ' + hyps_file + ' '
                                        + refs_file).split(),
                                       stdout=subprocess.PIPE)
            output, error = process.communicate()

        if metric == 'beer':
            scores.append([float(score.split()[-1])])
        else:
            scores.append([score.score])

    return scores


def get_segments(file):
    segments = {}
    order = []

    try:
        tree = ET.parse(file,  ET.XMLParser(recover=True))
    except IOError:
        sys.stderr.write('Error: ' + file + ' does not exist.\n')
        sys.exit(-1)
    except SyntaxError:
        sys.stderr.write('Error parsing ' + file + '.\n')
        sys.exit(-1)

    root = tree.getroot()
    for document in root:
        segs = []
        for tag in document:
            if tag.tag == 'hl' or tag.tag == 'p':
                for seg in tag:
                    if seg.text is None:
                        segs.append('')
                    else:
                        segs.append(seg.text.strip())
            elif tag.tag == 'seg':
                if tag.text is None:
                    segs.append('')
                else:
                    segs.append(tag.text.strip())
        if len(segs) > 0:
            segments[document.attrib['docid']] = segs
            order.append(document.attrib['docid'])

    return segments, order


def parse_args():
    parser = argparse.ArgumentParser(description='This script assesses\
                                     whether two systems present statistical\
                                     diferences in their performance.')
    parser.add_argument('-a', '--systema', metavar='system_a',
                        required=True, help='sgm file containing a participant\
                        translation hypothesis.')
    parser.add_argument('-b', '--systemb', metavar='system_b',
                        required=True, help='sgm file containing another \
                        participant translation hypothesis.')
    parser.add_argument('-r', '--references', metavar='references',
                        required=True, help='sgm file containing the \
                        references.')
    parser.add_argument('-t', '--trials', metavar='trials',
                        required=False, default=10000, help='number of trials\
                         to compute (default: 10000).', type=int)
    parser.add_argument('-p', '--pvalue', metavar='p-value',
                        required=False, default=0.05, help='p-value for \
                        assessing statistical significance (default: 0.05).',
                        type=float)
    parser.add_argument('-m', '--metric', metavar='metric',
                        choices=['bleu', 'ter', 'beer'], required=False,
                        default='bleu', help='metric to compute.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    ref, ref_order = get_segments(args.references)
    a, a_order = get_segments(args.systema)
    b, b_order = get_segments(args.systemb)

    a_scores = compute_metrics(ref, a, a_order, args.metric)
    b_scores = compute_metrics(ref, b, b_order, args.metric)

    print('Studying ' + args.metric + ' scores:')
    assess_differences(a_scores, b_scores, args.trials, args.pvalue)
