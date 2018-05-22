# Steven Atkinson
# satkinso@nd.edu
# May 22, 2018

from __future__ import absolute_import
import os


def main_file(dir):
    """
    Find the main file

    :param dir: project directory
    """
    main_file = dir + "/Main.tex"
    if not os.path.isfile(main_file):
        raise FileNotFoundError("Failed to find a main file in {}".format(dir))
    return main_file


def used_files(current_file, files=[]):
    """
    Get the files used by the current file and append them to the list.

    :param current_file: the file to search through
    :param files: Current list of files
    """
    raise NotImplementedError("")

