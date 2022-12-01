# Covid-19 MLIA: Machine Translation Task
This repository contains the official scripts used in the [Machine Translation (MT) task](http://eval.covid19-mlia.eu/task3/) from [Covid-19 MLIA](http://eval.covid19-mlia.eu/).

## Task Description
The goal of the MT task was to evaluate systems focused on the Covid-19 related text. The Covid-19 MT task addressed the following language pairs:

* English–German.
* English–French.
* English–Spanish.
* English–Italian.
* English–Modern Greek.
* English–Swedish.
* English–Arabic. (From round 2.)

The main challenge was that the text to be translated was specialized on the new and high-relevant topic of Covid-19. The task was open for beginners and established research groups from any area of interest in the scientific community, the public administration and the industry.

## Round 1

### Corpus generation
* [Data crawling, training and validation sets](round1/data).
* [Test sets](round1/tests).

### Evaluation scripts
* [Automatic evaluation](round1/evaluation).
* [Statistical differences](round1/art).

### Overview
* [Slides](https://mdomingo.me/presentations/COVID19MLIA2021.pdf).
* [Presentation](https://youtu.be/vZgNlEdX7XE?t=5510).

## Round 2

### Corpus generation
* [Data crawling](round2/data).
* [Training, validation and test sets](round2/partitions).

### Evaluation scripts
* [Automatic evaluation](round2/evaluation).
* [Statistical differences](round2/art).

### Overview
* [Slides](https://mdomingo.me/presentations/COVID19MLIA2022.pdf).
* [Presentation](https://youtu.be/C39UhuXMyNc?t=685).

## General utilities
* [SGM generator](sgm/generator).
* [SGM reader](sgm/reader).
* [Translation Memory eXchange reader](tmx).

## Findings
* [Rolling report](https://bitbucket.org/covid19-mlia/organizers-task3/src/master/report/report.pdf).
