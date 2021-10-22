# Statistical Significance (Round 1)
This repository contains the script used for assessing the statistical significance of the difference in performance between two systems according to BLEU and ChrF.

## Requirements
This script makes use of the following libraries, which can be installed through pip:
```
pip install lxml sacrebleu
```

## Usage
```
python statistical_differences.py [-h] -a system_a -b system_b -r references
                                  [-t trials] [-p p-value]

This script assesses whether two systems present statistical diferences in
their performance.

optional arguments:
  -h, --help            show this help message and exit
  -a system_a, --systema system_a
                        sgm file containing a participant translation
                        hypothesis.
  -b system_b, --systemb system_b
                        sgm file containing another participant translation
                        hypothesis.
  -r references, --references references
                        sgm file containing the references.
  -t trials, --trials trials
                        number of trials to compute (default: 10000).
  -p p-value, --pvalue p-value
                        p-value for assessing statistical significance
                        (default: 0.05).
```
