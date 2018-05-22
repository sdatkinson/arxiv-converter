# Steven Atkinson
# satkinso@nd.edu
# May 22, 2018


from __future__ import absolute_import
import convert
import sys

"""
Converter for arXiv
"""


if __name__ == "__main__":
    argc = len(sys.argv)
    if not argc == 2:
        print("Usage: main.py [project directory]")
    else:
        dir_from = sys.argv[1]
        
        # convert.check(dir_from)
        main_file = convert.main_file(dir_from)
        files = convert.used_files(main_file, [main_file])
        
        # Remove "embarrasing comments" using the perl command provided by 
        #   arXiv
        # Flatten file trees, replacing forward slashes with underscores
        # Checks for \usepackage{hyperref} and comments it out
        # Take all figures and create eps versions
        # Take all eps figures and create a pdf version that arXiv apparently
        #   needs
        # Remove all files that the project doesn't actually reference with
        #   \input or \includegraphics when creating the document
        # Test compiling the document

