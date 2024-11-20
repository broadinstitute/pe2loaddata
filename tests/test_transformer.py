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

def test_write_csv_from_remote():
    config_file = "tests/data/Remote/config_s3test.yml"

    assert os.path.exists(config_file)

    channels, metadata = load_config(config_file)

    channels = dict([(str(k).replace(" ", ""), v) for (k, v) in channels.items()])

    index_directory = "s3://cellpainting-gallery/cpg0001-cellpainting-protocol/source_4/images/2020_06_19_Stain2_Batch1/images/BR00113255__2020-06-19T11_13_27-Measurement2/Images/"
    index_file = "s3://cellpainting-gallery/cpg0001-cellpainting-protocol/source_4/images/2020_06_19_Stain2_Batch1/images/BR00113255__2020-06-19T11_13_27-Measurement2/Images/Index.idx.xml"

    import boto3
    s3 = boto3.client("s3")
    # Download index file to output directory
    bucket, index_file_key = index_file.split(f"s3://")[1].split("/",1)
    index_file = "Index.idx.xml"
    with open(index_file, "wb") as f:
        s3.download_fileobj(bucket, index_file_key, f)

    handler = Handler()

    xml.sax.parse(index_file, handler)

    images = handler.root.images.images
    plates = handler.root.plates.plates
    wells = handler.root.wells.wells
    maps = handler.root.maps.map_dict

    paths = {}

    index_directory_key = index_directory.split(f"s3://{bucket}/")[1]
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=index_directory_key)
    for page in pages:
        for x in page["Contents"]:
            fullpath = x["Key"]
            path, filename = fullpath.rsplit("/", 1)
            if filename.endswith(".tiff"):
                paths[filename] = path

    with open("example.csv", "w") as fd:
        writer = csv.writer(fd, lineterminator='\n')

        write_csv(writer, images, plates, wells, maps, channels, metadata, paths)

    gt = []
    created = []

    with open("tests/data/Remote/loaddata_cpg.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            gt.append(row)

    with open("example.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            created.append(row)

    assert gt == created
    
    os.remove("Index.idx.xml")
    os.remove("example.csv")