import csv
import os
import xml.sax
from os import PathLike
from pathlib import Path
from os import PathLike
import argparse
import pytest
from argparse import ArgumentTypeError, ArgumentParser, _StoreAction

from src.pe2loaddata.content import Handler


from src.pe2loaddata.append_illum_cols import check_file_arg, check_dir_arg, load_config, parse_args, main, write_csv

from typing import Union


def test_check_file_arg():
    pathname = __file__

    arg = check_file_arg(pathname)

    assert arg == arg

    try:
        check_file_arg("foo")

        assert False
    except ArgumentTypeError:
        assert True


def test_check_dir_arg():
    dirname = Path(__file__).parent

    arg = check_dir_arg(dirname)

    assert arg == arg

    try:
        check_dir_arg("foo")

        assert False
    except ArgumentTypeError:
        assert True

def test_load_config(test_files):
    pathname = test_files["config_file"]

    assert os.path.exists(pathname)

    channels = load_config(pathname)

    expected_channels = test_files["expected_channels"]

    assert channels == expected_channels



def test_parse_args():
    pass


def test_main(test_files):
    config_file = test_files["config_file"]
    input_csv = test_files["output_file"]
    illum_filetype = ".npy"
    nrows = sum(1 for _ in open(input_csv)) - 1

    expected_channels = test_files["expected_channels"]

    assert os.path.exists(config_file)
    channels = load_config(config_file)
    illum_directory = "tests/data/illum/"
    plate_id = "BR00121482"

    assert nrows !=  {}
    assert channels == expected_channels



    with open('illum.csv', 'w') as fd:
        writer = csv.writer(fd, lineterminator='\n')
        write_csv(writer, channels, illum_directory, plate_id, nrows, illum_filetype)
    
    os.remove('illum.csv')

def test_write_csv(test_files):
    config_file = test_files["config_file"]
    input_csv = test_files["output_file"]
    illum_filetype = ".npy"

    nrows = sum(1 for _ in open(input_csv)) - 1

    channels = load_config(config_file)
    illum_directory = "tests/data/illum/"
    plate_id = "BR00121482"

    with open('illum.csv', 'w') as fd:
        writer = csv.writer(fd, lineterminator='\n')

        write_csv(writer, channels, illum_directory, plate_id, nrows, illum_filetype)

    os.remove('illum.csv')

















