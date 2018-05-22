# arxiv-converter #
Take LaTeX projects and convert them to a version that is arXiv-ready
If your project is in a directory `my-paper`, this creates an arXiv-ready version in `my-paper-arxiv-version`

## Steps this takes: ##
* [TODO] Remove "embarrasing comments" using the perl command provided by arXiv
* [TODO] Flatten file trees, replacing forward slashes with underscores
* [TODO] Checks for \usepackage{hyperref} and comments it out
* [TODO] Take all figures and create eps versions
* [TODO] Take all eps figures and create a pdf version that arXiv apparently needs
* [TODO] Remove all files that the project doesn't actually reference with \input or \includegraphics when creating the document
* [TODO] Test compiling the document
