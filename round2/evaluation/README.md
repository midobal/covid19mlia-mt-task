# Automatic Evaluation (Round 2)
This repository contains the evaluation script used for computing the automatic evaluation of translations submitted by the participants on round 2.

## Requirements
This script makes use of the following libraries, which can be installed through pip:
```
pip install lxml sacrebleu
```

Additionally, you need to download [Beer](https://github.com/stanojevic/beer) on the same directory as this script:
```
wget https://raw.githubusercontent.com/stanojevic/beer/master/packaged/beer_2.0.tar.gz
tar xfvz beer_2.0.tar.gz; rm beer_2.0.tar.gz
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
team_name {constrained,unconstrained} system_description_from_free_field bleu_score ter_score beer_score
```
