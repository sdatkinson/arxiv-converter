# Steven Atkinson
# satkinso@nd.edu
# May 22, 2018


from __future__ import absolute_import
import convert
import sys
import os
import argparse
from shutil import copyfile

"""
Converter for arXiv
"""


if __name__ == "__main__":
    argc = len(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument("src_dir", help="Home direcotry for the project")
    parser.add_argument(
        "-d", "--dest_dir",
        help="Directory the converted project will be written to")
    parser.add_argument("-o", "--overwrite",
                        help="allow overwriting the destination directory",
                        action="store_true")
    args = parser.parse_args()
    args.dest_dir = args.dest_dir or args.src_dir + "-converted"

    if os.path.isdir(args.dest_dir) and not args.overwrite:
        raise RuntimeError("Target directory {} already exists".format(
            args.dest_dir))

    # convert.check(dir_from)
    main_file = convert.main_file(args.src_dir)
    files = convert.needed_files(args.src_dir, main_file)

    # Make the destination directory and copy the main file:
    os.makedirs(args.dest_dir)
    copyfile(args.src_dir + "/" + main_file, args.dest_dir + "/" + main_file)

    # Paste the input files into main (resulting in a single .tex file for the
    # project)

    # Remove "embarrassing comments" using the perl command provided by
    # arXiv

    # Flatten file trees, replacing forward slashes with underscores

    # Checks for \usepackage{hyperref} and comments it out

    # Take all figures and create eps versions

    # Take all eps figures and create a pdf version that arXiv apparently
    # needs

    # Remove all files that the project doesn't actually reference with
    # \input or \includegraphics when creating the document

    # Test compiling the document

