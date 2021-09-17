#!/usr/bin/env python
import argparse
import sys
import os
import lxml.etree as ET
import sacrebleu
import subprocess
import time


def save_to_file(sentences):
    file = '/tmp/' + str(time.time()) + '_covid19mlia'
    with open(file, 'w') as f:
        f.write('\n'.join(sentences))
    return file


def compute_metrics(ref, hyp, hyp_order):
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

    # Compute BLEU and TER
    try:
        bleu = sacrebleu.corpus_bleu(hyps, [refs])
        ter = sacrebleu.corpus_ter(hyps, [refs])
    except EOFError:
        sys.stderr.write('Error: source and reference have different'
                         + ' lengths.\n')
        sys.exit(-1)

    # Create aux files for BEER
    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    hyps_file = save_to_file(hyps)
    refs_file = save_to_file(refs)

    # Compute BEER
    process = subprocess.Popen((dir + '/beer_2.0/beer -s ' + hyps_file + ' -r '
                                + refs_file).split(), stdout=subprocess.PIPE)
    beer, error = process.communicate()

    # Delete aux files
    process = subprocess.Popen(('rm ' + hyps_file + ' '
                                + refs_file).split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    return bleu.score, ter.score, float(beer.split()[-1])


def get_participant_data(file):
    name = os.path.basename(file).split('.')[0].split('_')
    if len(name) != 6:
        sys.stderr.write('Error: translation file is not using '
                         + 'the proper name convention.\n')
        sys.exit(-1)
    team = name[0]
    language = name[3]
    type = name[-2]
    approach = name[-1]
    return team, language, type, approach


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
    team, language, type, approach = get_participant_data(args.translations)

    bleu, ter, beer = compute_metrics(ref, hyp, hyp_order)

    print(f'{team} {language} {type} {approach} {bleu:.1f} {ter * 100:.1f}'
          + ' ' + f'{beer * 100:.1f}')
