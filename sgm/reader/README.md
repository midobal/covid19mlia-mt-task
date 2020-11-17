# Standard Generalized Markup Language Reader
This repository includes a script for extracting segments from a sgm file.

## Requirements
This script makes use of 'xml', which can be installed through pip:
```
pip install lxml
```

## Usage
```
python sgm_reader.py [-h] -f sgm_file [-o output_file]

This script extracts segments from a sgm file.

optional arguments:
  -h, --help            show this help message and exit
  -f sgm_file, --file sgm_file
                        sgm file from which to extract the segments.
  -o output_file, --output output_file
                        file in which to store the segment. (Default: create
                        documents using the docid from the sgm.)
```
