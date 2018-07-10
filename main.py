# Steven Atkinson
# satkinso@nd.edu
# May 22, 2018


from __future__ import absolute_import
import convert
import sys
import os
import argparse
import shutil

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
    parser.add_argument(
        "--keep-hyperref",
        help="Prevents from deleting the line that includes the hyperref " +
             "package", action="store_true")
    args = parser.parse_args()
    args.dest_dir = args.dest_dir or args.src_dir + "-converted"

    if os.path.isdir(args.dest_dir):
        if args.overwrite:
            shutil.rmtree(args.dest_dir)
        else:
            raise RuntimeError("Target directory {} already exists".format(
                args.dest_dir))
    os.makedirs(args.dest_dir)

    # convert.check(dir_from)
    main_file = convert.main_file(args.src_dir)
    src_files = convert.needed_files(args.src_dir, main_file)

    # Paste the input files into main (resulting in a single .tex file for the
    # project)
    tex_lines = convert.insert_inputs(args.src_dir, main_file)

    # Remove comments
    # TODO also comments that end a line
    tex_lines = convert.remove_comments(tex_lines)

    # Flatten figure files, replacing forward slashes with underscores
    # The naming convention is "fig1.pdf", "fig2.eps", etc.
    tex_lines, dest_fig_files = convert.clean_figs(tex_lines)

    # Checks for \usepackage{hyperref} and removes it.
    if not args.keep_hyperref:
        tex_lines = convert.remove_hyperref(tex_lines)

    # Write the file:
    convert.write_lines_to(tex_lines, args.dest_dir + "/" + main_file)

    # Move the figures:
    for fig_from, fig_to in zip(src_files["figs"], dest_fig_files):
        shutil.copyfile(args.src_dir + "/" + fig_from,
                        args.dest_dir + "/" + fig_to)
    # Move the bib:
    n_bibs = len(src_files["bib"])
    if n_bibs == 1:
        shutil.copyfile(args.src_dir + "/" + src_files["bib"][0],
                        args.dest_dir + "/" + src_files["bib"][0])
    elif n_bibs > 1:
        RuntimeError("More than 1 bib found?")

    # Take all eps figures and create a pdf version?

    # Test compiling the document...

