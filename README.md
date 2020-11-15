# Covid-19 MLIA: MT Evaluation
This repository contains the evaluation script used in the [MT task](http://eval.covid19-mlia.eu/task3/) from [Covid-19 MLIA](http://eval.covid19-mlia.eu/).

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
team_name {constrained,unconstrained} system_description_from_free_field bleu ter
```
