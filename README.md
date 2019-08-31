# arxiv-converter #
[![CircleCI](https://circleci.com/gh/sdatkinson/arxiv-converter.svg?style=svg)](https://circleci.com/gh/sdatkinson/arxiv-converter)

Take LaTeX projects and convert them to a version that is arXiv-ready
If your project is in a directory `my-paper`, this creates an arXiv-ready
version in `my-paper-converted`

## Requirements ##
* Need to be able to call pdflatex and bibtex with `subprocess.call()`

## Steps this takes: ##
* Remove lines that are comments (TODO: comments that are at the end of a line")
* Move all text into a single .tex file
* Compiles the document to generate the .bbl, then inserts it into the tex file.
* Checks for \usepackage{hyperref} and comments it out
* Flatten all figures to "fig1.eps", etc
* Take all eps figures and create a pdf version
* Checks whether all files total to less than 10 MB
