# Steven Atkinson
# satkinso@nd.edu
# May 22, 2018

from __future__ import absolute_import
import os
import re
from subprocess import call


# Regular expressions
# Comments:
_comment_re = re.compile("^\s{0,}%")
# for \input lines:
_input_re = re.compile("\\\\input\\{[0-9a-zA-Z\/\_]{1,}(\.tex)?\}")
# For graphics:
# Only support eps and pdf for now.  If you want other formats, then we also
# need to be able to convert them to pdfs.
_graphics_re = re.compile("\\\\includegraphics" +
                          "(\[[0-9a-zA-Z,\s\-\=\.\\\\]{1,}\])?" +  # [width=stuff]
                          "\{[a-zA-Z0-9\/\_\.]{1,}" +  # Filename
                          "[(\.eps)(\.pdf)]\}")
_bibliography_re = re.compile("\\\\bibliography\{[a-zA-Z0-9\/\_\.]{1,}\}")


def main_file(dir):
    """
    Find the main file
    Currently only supports Main.tex or main.tex

    MUST END IN .tex!

    :param dir: project directory
    """
    possible_main_files = {"Main.tex", "main.tex"}
    for main_file in possible_main_files:
        mf_with_dir = dir + "/" + main_file
        if os.path.isfile(mf_with_dir):
            print("Found main file at {}".format(mf_with_dir))
            return main_file
    raise FileNotFoundError("Failed to find a main file in {}".format(dir))


def read_file(fname):
    with open(fname) as f:
        lines = f.readlines()
    return lines


def line_is_comment(line):
    return bool(re.search(_comment_re, line))


def get_input_file(line):
    if not line_is_comment(line) and re.search(_input_re, line):
        line = line.strip()
        new_file = line[7:-1]  # Assumes \input{file.tex}\n
        if not new_file[-4:] == ".tex":
            new_file += ".tex"
        return new_file
    else:
        return None


def get_graphics_file(line):
    if not line_is_comment(line) and re.search(_graphics_re, line):
        graphics_string = re.search(_graphics_re, line).string
        graphics_string = graphics_string.strip()
        new_file = graphics_string[graphics_string.find("{") + 1: -1]
        return new_file
    else:
        return None


def get_bibliography_file(line):
    """
    e.g. \bibliography{References} returns "References.bib"
    :param line:
    :return:
    """
    if not line_is_comment(line) and re.search(_bibliography_re, line):
        bib_string = re.search(_bibliography_re, line).string.strip()
        new_file = bib_string[bib_string.find("{") + 1: -1]
        if not new_file[-4:] == ".bib":
            new_file += ".bib"
        return new_file
    else:
        return None


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

    lines = read_file(dir + "/" + current_file)
    file_set = {"figs": [], "bib": []}
    for line in lines:
        # Search for \input calls and descend recursively
        inputted_file = get_input_file(line)
        if inputted_file:
            child_file_set = needed_files(dir, inputted_file)
            file_set["figs"] += child_file_set["figs"]
            file_set["bib"] += child_file_set["bib"]
        # Search for figures included
        graphics_file = get_graphics_file(line)
        if graphics_file:
            file_set["figs"] += [graphics_file]
        bibliography_file = get_bibliography_file(line)
        if bibliography_file:
            file_set["bib"] += [bibliography_file]
    return file_set


def insert_inputs(src_dir, current_file):
    """
    Take a file and recursively paste in all of the content that is \input'ed

    :param src_file:
    :param dest_dir:
    :return:
    """
    lines = read_file(src_dir + "/" + current_file)
    i = 0
    while i < len(lines):
        line = lines[i]
        inputted_file = get_input_file(line)  # TODO replace w/ recursive call
        if inputted_file:
            inputted_lines = ["% Inputted from {}\n".format(inputted_file)] + \
                             read_file(src_dir + "/" + inputted_file) + \
                             ["\n"]
            # Replace the \input line with the file:
            lines = lines[:i] + inputted_lines + lines[i + 1:]
            # Notice: we just pasted in the file--which may have its own
            # "\input"s.  So, this will automatically "recurse" because we're
            # inserting them ahead of "i"
        i += 1
    return lines


def remove_comments(lines):
    return [line for line in lines if not line_is_comment(line)]


def clean_figs(lines, pdfs_only):
    """
    Go through the document, and whenever you see a figure included,

    * Rename that figure to "fig1.pdf", "fig2.pdf", etc
    * Make a note of the new name (with the old type).  We will convert eps'es
        to pdfs later.

    :param lines: The tex document
    :type lines: list of strings
    :param pdfs_only: if true, require that all figures end up as pdfs.
    :type pdfs_only: bool

    :return: revised tex document, list of new figures.
    """
    fig_name_new_list = []
    for i in range(len(lines)):
        line = lines[i]
        g_file_from = get_graphics_file(line)
        if g_file_from:
            fig_count = len(fig_name_new_list) + 1
            j = g_file_from.rfind(".")
            fig_type = g_file_from[j + 1:]
            fig_name_new_old_type = "fig{}.{}".format(fig_count, fig_type)
            fig_name_new_new_type = "fig{}.pdf".format(fig_count) if pdfs_only \
                else fig_name_new_old_type
            line = line.replace(g_file_from, fig_name_new_new_type)
            lines[i] = line
            fig_name_new_list += [fig_name_new_old_type]
    return lines, fig_name_new_list


def epss_to_pdfs(dest_dir, fig_files):
    """
    Convert any non-pdfs to pdfs.

    :param dest_dir:
    :param fig_files:
    :return:
    """
    print("Converting figures to pdfs")
    for i in range(len(fig_files)):
        f0 = fig_files[i]
        print("{} / {}".format(i + 1, len(fig_files)))
        if not f0[-4:] == ".pdf":
            call(["epstopdf", dest_dir + "/" + f0])
            os.remove(dest_dir + "/" + f0)
            fig_files[i] = f0[:-4] + ".pdf"
    return fig_files


def insert_bbl(lines, bbl_fname):
    bbl_lines = read_file(bbl_fname)
    i = 0
    while i < len(lines):
        line = lines[i]
        if get_bibliography_file(line):
            lines = lines[:i] + ["% Added from bbl:\n"] + bbl_lines + \
                    lines[i + 1:]
        else:
            i += 1
    return lines


def comment_hyperref(lines_in):
    lines = lines_in.copy()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "\\usepackage{hyperref}":
            lines[i] = "% " + lines[i]
        i += 1
    return lines


def write_lines_to(lines, fname):
    s = ""
    for line in lines:
        s += line
    with open(fname, "w") as f:
        f.write(s)
        return
