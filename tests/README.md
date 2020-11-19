# Generation of the Test Sets

## Round 1

### Data crawling
Description of how the data was crawl will be added at a later date.

### Data selection
Given the set of *.file* documents obtained from the data crawling, for each language pair, we created a new document (`scored_test`) composed of:
```
alignment_score source_segment target_segment file_name
```
where:
* *alignment_score* is the alignment probability for those to segments.
* *source_segment* is the segment in the source language.
* *target_segment* is the segment in the target language.
* *file_name* is the *.filt* file from which the segment was obtained.

(Tabs are used for separating fields.)

This document was created using the following command:
```
for f in *.filt; do awk -F "\t" '{print $1"\t"$2"\t"$3"\t"FILENAME}' $f; done | \
sort -g -r > scored_test
```

Finally, out of all the available segments (from each of the `scored_test` documents from each language pair), we selected for each language pair the best 2000 segments by doing:
```
python select.py scored_test average_segment_length
```
where `average_sentence_length` is the average number of words per segment from the training data set.

### SGM generation
We generated the sgm files for the documents obtained from the data selection using the [sgm generator](https://github.com/midobal/covid19mlia-mt-task/tree/master/sgm/generator):
```
for tgt in de el es fr it sv; do python sgm_generator.py -f en-${tgt}/test.en \
--id round1_test -t source -o test-en${tgt}-src.en.sgm; done

for tgt in de el es fr it sv; do python sgm_generator.py -f en-${tgt}/test.${tgt} \
--id round1_test -t reference -o test-en${tgt}-ref.${tgt}.sgm; done
```
