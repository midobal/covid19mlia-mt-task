# Standard Generalized Markup Language Generator
This repository includes a script for generating a sgm file from one or more text files.

## Requirements
This script makes use of 'xml', which can be installed through pip:
```
pip install lxml
```

## Usage
```
python sgm_generator.py [-h] -f text_files [text_files ...] -o sgm_file
                        [-i id] -t {source,translation,reference}

This script generates an sgm file.

optional arguments:
  -h, --help            show this help message and exit
  -f text_files [text_files ...], --files text_files [text_files ...]
                        text files to convert into sgm.
  -o sgm_file, --output sgm_file
                        file in which to store the sgm.
  -i id, --id id        id to use as the docid of the sgm. (Default: test.)
  -t {source,translation,reference}, --type {source,translation,reference}
                        type of document.
```
