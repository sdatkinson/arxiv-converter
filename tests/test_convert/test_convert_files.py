# File: test_convert_files.py
# File Created: Saturday, 31st August 2019 12:30:20 pm
# Author: Steven Atkinson (steven@atkinson.mn)

import os
import sys

import pytest

_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(_file_dir, "..", ".."))

import convert

_paper_dir = os.path.join(_file_dir, "mypaper")


def test_main_file():
    res = convert.main_file(_paper_dir)
    assert isinstance(res, str)
    assert res == "main.tex"


def test_read_file():
    lines = convert.read_file(os.path.join(_paper_dir, "section.tex"))
    assert isinstance(lines, list)
    assert all([isinstance(l, str) for l in lines])
