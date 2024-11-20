import csv
import os.path
import xml.sax
from argparse import ArgumentTypeError
from pathlib import Path

from src.pe2loaddata.content import Handler
from src.pe2loaddata.transformer import check_file_arg, check_dir_arg, load_config, write_csv


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
    directory = Path(__file__).parent

    arg = check_dir_arg(directory)

    assert arg == arg

    try:
        check_dir_arg(__file__)

        assert False
    except ArgumentTypeError:
        assert True

    try:
        check_dir_arg("foo")

        assert False
    except ArgumentTypeError:
        assert True


def test_parse_args():
    pass


def test_load_config(test_files):
    pathname = test_files["config_file"]

    assert os.path.exists(pathname)

    channels, metadata = load_config(pathname)

    expected_channels = test_files["expected_channels"]

    expected_metadata = {
        "AbsPositionZ": "AbsPositionZ",
        "AbsTime": "AbsTime",
        "BinningX": "BinningX",
        "BinningY": "BinningY",
        "ChannelID": "ChannelID",
        "ChannelName": "ChannelName",
        "Col": "Col",
        "ExposureTime": "ExposureTime",
        "FieldID": "FieldID",
        "ImageResolutionX": "ImageResolutionX",
        "ImageResolutionY": "ImageResolutionY",
        "ImageSizeX": "ImageSizeX",
        "ImageSizeY": "ImageSizeY",
        "MainEmissionWavelength": "MainEmissionWavelength",
        "MainExcitationWavelength": "MainExcitationWavelength",
        "MaxIntensity": "MaxIntensity",
        "ObjectiveMagnification": "ObjectiveMagnification",
        "ObjectiveNA": "ObjectiveNA",
        "PlaneID": "PlaneID",
        "PositionX": "PositionX",
        "PositionY": "PositionY",
        "PositionZ": "PositionZ",
        "Row": "Row"
    }

    assert channels == expected_channels
    assert metadata == expected_metadata


def test_write_csv(test_files):
    config_file = test_files["config_file"]

    assert os.path.exists(config_file)

    channels, metadata = load_config(config_file)

    channels = dict([(str(k).replace(" ", ""), v) for (k, v) in channels.items()])

    index_file = test_files["index_file"]

    handler = Handler()

    xml.sax.parse(index_file, handler)

    images = handler.root.images.images
    plates = handler.root.plates.plates
    wells = handler.root.wells.wells
    maps = handler.root.maps.map_dict

    paths = {}

    index_directory = test_files["index_directory"]

    for filename in os.listdir(index_directory):
        paths[filename] = index_directory

    with open("example.csv", "w") as fd:
        writer = csv.writer(fd, lineterminator='\n')

        write_csv(writer, images, plates, wells, maps, channels, metadata, paths)

    gt = []
    created = []

    with open(test_files["output_file"]) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            gt.append(row)

    with open("example.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            created.append(row)

    assert gt == created
    
    os.remove("example.csv")
