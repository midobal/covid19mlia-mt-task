#!/bin/bash


REF=$1
TRANS=$2

source /home/ubuntu/eval_competition/venv3.7/bin/activate


python /home/ubuntu/eval_competition/covid19mlia-mt-evaluation/evaluation/evaluate.py -r $REF -t $TRANS 
#pangeanic en2es constrained bt 53.2 0.733

