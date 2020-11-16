#!/usr/bin/env python
import argparse
import sys
import os
import lxml.etree as ET
import sacrebleu


def compute_metrics(ref, hyp, hyp_order):
    refs = []
    hyps = []
    for id in hyp_order:
        for segment in hyp[id]:
            hyps.append(segment)
        try:
            for segment in ref[id]:
                refs.append(segment)
        except KeyError:
            sys.stderr.write('Error: reference not found for segment'
                             + ' "' + segment + '"\n')
            sys.exit(-1)
    bleu = sacrebleu.corpus_bleu(hyps, [refs])
    chrf = sacrebleu.corpus_chrf(hyps, [refs])
    return bleu.score, chrf.score


def get_participant_data(file):
    name = os.path.basename(file).split('.')[0].split('_')
    if len(name) != 6:
        sys.stderr.write('Error: translation file is not using '
                         + 'the proper name convention.\n')
        sys.exit(-1)
    team = name[0]
    type = name[-2]
    approach = name[-1]
    return team, type, approach


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
                    segs.append(seg.text.strip())
        if len(segs) > 0:
            segments[document.attrib['docid']] = segs
            order.append(document.attrib['docid'])

    return segments, order


def parse_args():
    parser = argparse.ArgumentParser(description='This script evaluates\
                                     a participants translations.')
    parser.add_argument('-t', '--translations', metavar='translations',
                        required=True, help='sgm file containing a participant\
                        translation hypothesis.')
    parser.add_argument('-r', '--references', metavar='references',
                        required=True, help='sgm file containing the \
                        references.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    ref, ref_order = get_segments(args.references)
    hyp, hyp_order = get_segments(args.translations)
    team, type, approach = get_participant_data(args.translations)

    bleu, chrf = compute_metrics(ref, hyp, hyp_order)

    print(f'{team} {type} {approach} {bleu:.1f} {chrf:.3f}')
