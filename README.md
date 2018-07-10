# arxiv-converter #
Take LaTeX projects and convert them to a version that is arXiv-ready
If your project is in a directory `my-paper`, this creates an arXiv-ready version in `my-paper-converted`

## Steps this takes: ##
* Remove lines that are comments (TODO: comments that are at the end of a line")
* Move all text into a single .tex file
* Checks for \usepackage{hyperref} and comments it out
* Flatten all figures to "fig1.eps", etc
* [TODO?] Take all eps figures and create a pdf version

You can test compiling the document locally with the --keep-hyperref argument.
