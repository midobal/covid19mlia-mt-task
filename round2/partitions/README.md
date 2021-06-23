# Generation of the Training, Validation and Test Sets
Given the collection of *tsv* files obtained from the [data crawling](../data), we analyzed the data and split it into *training*, *validation* and *test*.

## Filtering
The first step we took was to analyze the data by computing a histogram:

```
word_histogram.py [-h] -f files [files ...] -o image -t title
                         [-l lower] [-u upper]

This script generates a histogram of the number of words per sentence in a
given document.

optional arguments:
  -h, --help            show this help message and exit
  -f files [files ...], --files files [files ...]
                        document to analyze.
  -o image, --output image
                        image containing the instagram.
  -t title, --title title
                        title for the histogram.
  -l lower, --lower lower
                        lower interval, around the mean, in which to center
                        the histogram.: lower * mean. (Default: no limit.)
  -u upper, --upper upper
                        upper interval, around the mean, in which to center
                        the histogram.: upper * mean. (Default: no limit.)
```

With this, we took the decission to remove all segments which contained more than 100 words (either in the source or the target) since they were outliers. Additionally, we observed that the most representative subset for which to select the validation and test sets is: [0.7 * average_words_per_segment, 1.3 * average_words_per_segment].

## Partitions
Since the data came from different sources, we wanted to ensure that both the validation and tests sets were representative enough of the training sets. For this reasons, for each languag pair, we computed the representation of each source in the total data (i.e., the number of segments from this source divided by the total number of segments). Then, out of the total segments we wanted to select for validation and test (4000 for each), we select that same percentage from each source.

Adittionaly, to ensure that validation and test did not contained low-quality segments (rembember that the data has been crawled from the web), we sorted the segments acording to its alignment quality (which is included in the *tsv* files). Finally, we shuffled the selected segments and split them equally into validation and test.

Therefore, the procedure we followed for each language pair was:

1. We computed the representation (%) of data from each different source over the total data.
2. We computed the average number of words per segment over this set.
3. We established a subset [0.7 * average_words_per_segment, 1.3 * average_words_per_segment].
4. We sorted this subset (from best to worst) according to its alignment quality.
5. We selected the best 8000 * the percentage obtained at step 1 segments.
6. We shuffled those segments and select half of them for validation and the other half for test.

These procedure was done using the following script:

```
get_partitions.py [-h] -f files [files ...] [-l lower] [-u upper]
                         [-w max_words] [-n n_segments] -s source_language -t
                         target_language

This script generates train, dev and test partitions (in tmx) from a set of
tsv files.

optional arguments:
  -h, --help            show this help message and exit
  -f files [files ...], --files files [files ...]
                        tsv files containing the data.
  -l lower, --lower lower
                        lower interval for selecting dev and test: lower *
                        mean. (Default: 0.7.)
  -u upper, --upper upper
                        upper interval for selecting dev and test: upper *
                        mean. (Default: 1.3.)
  -w max_words, --max_words max_words
                        maximum number of words per segment. (Default: no
                        limit.)
  -n n_segments, --n_segments n_segments
                        maximum number of words per segment. (Default: no
                        limit.)
  -s source_language, --src source_language
                        source language.
  -t target_language, --tgt target_language
                        target language.
```
