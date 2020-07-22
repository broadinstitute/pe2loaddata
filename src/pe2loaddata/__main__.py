import csv
import logging
import logging.config
import os
import xml.sax
import json

import pkg_resources

import src.pe2loaddata.content.document_handler
from . import pe2loaddata


def logging_config():
    pathname = os.path.join("data", "logging_config.json")

    return pkg_resources.resource_string(__name__, pathname)


def main():
    logging.config.dictConfig(json.load(logging_config()))

    options = pe2loaddata.parse_args()
    channels, metadata = pe2loaddata.load_config(options.config_file)

    # Strip spaces because XML parser is broken
    channels = dict([(str(k).replace(" ", ""), v) for (k, v) in channels.items()])

    if not options.index_file:
        options.index_file = os.path.join(options.index_directory, "Index.idx.xml")

    doc = src.pe2loaddata.content.document_handler.DocumentHandler()

    xml.sax.parse(options.index_file, doc)

    images = doc.root.images.images
    plates = doc.root.plates.plates
    wells = doc.root.wells.wells
    paths = {}
    if options.search_subdirectories:
        for dir_root, directories, filenames in os.walk(options.index_directory):
            for filename in filenames:
                if filename.endswith(".tiff"):
                    paths[filename] = dir_root
    else:
        for filename in os.listdir(options.index_directory):
            paths[filename] = options.index_directory

    with open(options.output_csv, "wb") as fd:
        writer = csv.writer(fd, lineterminator='\n')
        pe2loaddata.write_csv(writer, images, plates, wells, channels, metadata, paths)
