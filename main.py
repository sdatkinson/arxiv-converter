# Steven Atkinson
# satkinso@nd.edu
# May 22, 2018


from __future__ import absolute_import
import convert
import sys
import os
import argparse
import shutil
from subprocess import call

"""
Converter for arXiv
"""


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("src_dir", help="Home directory for the project")
    parser.add_argument(
        "-d", "--dest_dir",
        help="Directory the converted project will be written to")
    parser.add_argument("-o", "--overwrite",
                        help="allow overwriting the destination directory",
                        action="store_true")
    parser.add_argument(
        "--remove-hyperref",
        help="comment out the use of the hyperref package", action="store_true")
    # parser.add_argument("--pdf-figs-only", help="convert all figures to pdf",
    #                     action="store_true")
    args = parser.parse_args()
    if args.dest_dir is None:
        args.dest_dir = args.src_dir + "-converted"
    
    return args


if __name__ == "__main__":
    args = _parse_args()

    # ===

    if os.path.isdir(args.dest_dir):
        if args.overwrite:
            shutil.rmtree(args.dest_dir)
        else:
            raise RuntimeError("Target directory {} already exists".format(
                args.dest_dir))
    os.makedirs(args.dest_dir)

    main_file = convert.main_file(args.src_dir)
    dest_file = args.dest_dir + "/" + main_file
    main_file_with_href = main_file[:-4] + "_with_href.tex"
    src_files = convert.needed_files(args.src_dir, main_file)

    # Paste the input files into main (resulting in a single .tex file for the
    # project)
    tex_lines = convert.insert_inputs(args.src_dir, main_file)

    # Remove comments
    # TODO also comments that end a line
    tex_lines = convert.remove_comments(tex_lines)

    # Flatten figure files, replacing forward slashes with underscores
    # The naming convention is "fig1.pdf", "fig2.eps", etc.
    tex_lines_with_href, dest_fig_files = convert.clean_figs(tex_lines, True)
    # args.pdf_figs_only)

    # Checks for \usepackage{hyperref} and comments it out.
    tex_lines = convert.comment_hyperref(tex_lines_with_href) \
        if args.remove_hyperref else tex_lines_with_href.copy()

    # Write the file with hyperref:
    convert.write_lines_to(tex_lines_with_href, args.dest_dir + "/" +
                           main_file_with_href)

    # Move the figures:
    for fig_from, fig_to in zip(src_files["figs"], dest_fig_files):
        shutil.copyfile(args.src_dir + "/" + fig_from,
                        args.dest_dir + "/" + fig_to)

    # Convert eps'es to pdfs:
    dest_fig_files = convert.epss_to_pdfs(args.dest_dir, dest_fig_files)

    # Move the bib:
    n_bibs = len(src_files["bib"])
    if n_bibs == 1:
        shutil.copyfile(args.src_dir + "/" + src_files["bib"][0],
                        args.dest_dir + "/" + src_files["bib"][0])
    elif n_bibs > 1:
        RuntimeError("More than 1 bib found?")

    # Compile to get the bbl:
    assert call(["pdflatex", main_file_with_href], cwd=args.dest_dir) == 0, \
        "Failed to compile .tex"
    assert call(["bibtex", main_file_with_href[:-4]], cwd=args.dest_dir) == 0, \
        "Failed to generate .bbl"

    # Insert the bbl:
    tex_lines = convert.insert_bbl(
        tex_lines, args.dest_dir + "/" + main_file_with_href[:-4] + ".bbl")

    # Write the tex file w/o hyperref and w/ bbl inserted.
    convert.write_lines_to(tex_lines, dest_file)

    # Remove unneeded files (i.e. from compilation...)
    print("Clean up destination directory")
    cleanup_files = [args.dest_dir + "/" + f for f in os.listdir(args.dest_dir)
         if not f == main_file and not f in dest_fig_files]
    [(lambda x: os.remove(x))(x) for x in cleanup_files]

    # Ensure 10MB size requirement:
    doc_size_mb = sum(os.path.getsize(args.dest_dir + "/" + f)
                      for f in os.listdir(args.dest_dir)
                      if os.path.isfile(args.dest_dir + "/" + f)) / 1e6
    assert doc_size_mb <= 10, "Document is too large ({}MB)".format(
        doc_size_mb)

    # Test compiling the document...
