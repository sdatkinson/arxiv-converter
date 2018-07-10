# Steven Atkinson
# satkinso@nd.edu
# May 22, 2018

from __future__ import absolute_import
import os
import re


def main_file(dir):
    """
    Find the main file
    Currently only supports Main.tex or main.tex

    :param dir: project directory
    """
    possible_main_files = set((
        "Main.tex",
        "main.tex"
    ))
    for main_file in possible_main_files:
        mf_with_dir = dir + "/" + main_file
        if os.path.isfile(mf_with_dir):
            print("Found main file at {}".format(mf_with_dir))
            return main_file
    raise FileNotFoundError("Failed to find a main file in {}".format(dir))


def needed_files(dir, current_file):
    """
    Get the files used by the current file and append them to the list.
    Searches for the following sorts of lines:
    * \input{file.tex}
    * \includegraphics[width=3]{MyFigure.eps}  # eps, pdf, png, jpg
    Assumes that the \input{} command is all on one line the ONLY thing on its line.

    :param current_file: the file to search through
    :param files: Current list of files
    """

    with open(dir + "/" + current_file) as f:
        lines = f.readlines()
    # Strip newlines:
    lines = [x.strip() for x in lines]

    # Regular expressions
    # Comments:
    comment_re = re.compile("^\s{0,}%")
    # for \input lines:
    input_re = re.compile("\\\\input\\{[0-9a-zA-Z\/\_]{1,}(\.tex)?\}")
    # For graphics:
    graphics_re = re.compile("\\\\includegraphics" +
                             "(\[[0-9a-zA-Z\=\.\\\\]{1,}\])?" + # [width=stuff]
                             "\{[a-zA-Z0-9\/\_\.]{1,}" +  # Filename
                             "[(\.eps)(\.pdf)(\.png)(\.jpg)]\}")

    child_files = set()
    for line in lines:
        # Skip comments
        if re.search(comment_re, line):
            continue
        # Search for \input calls and descend recursively
        if re.search(input_re, line):
            new_file = line[7:-1]  # Assumes \input{file.tex}\n
            if not new_file[-4:] == ".tex":
                new_file += ".tex"
            child_files = child_files.union(needed_files(dir, new_file))
        # Search for figures included
        if re.search(graphics_re, line):
            graphics_string = re.search(graphics_re, line).string
            new_file = graphics_string[graphics_string.find("{") + 1: -1]
            child_files = child_files.union(set((new_file,)))

    return set((current_file,)).union(child_files)
