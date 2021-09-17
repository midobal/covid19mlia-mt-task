# Automatic Evaluation (Round 1)
This repository contains the evaluation script used for computing the automatic evaluation of translations submitted by the participants on round 1.

## Requirements
This script makes use of the following libraries, which can be installed through pip:
```
pip install lxml sacrebleu
```

## Usage
```
python evaluate.py [-h] -t translations -r references

This script evaluates a participants translations.

optional arguments:
  -h, --help            show this help message and exit
  -t translations, --translations translations
                        sgm file containing a participant translation
                        hypothesis.
  -r references, --references references
                        sgm file containing the references.
```

## Output
```
team_name {constrained,unconstrained} system_description_from_free_field bleu_score chrf_score
```
