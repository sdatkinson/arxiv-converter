# File: test_convert_files.py
# File Created: Saturday, 31st August 2019 12:30:20 pm
# Author: Steven Atkinson (steven@atkinson.mn)

import os
import sys

import pytest

_file_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(_file_dir, "..", ".."))

import convert


def test_main_file():
    res = convert.main_file(os.path.join(_file_dir, "mypaper"))
    assert isinstance(res, str)
    assert res == "main.tex"
