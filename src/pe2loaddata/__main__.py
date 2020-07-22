import csv
import logging
import logging.config
import os
import xml.sax
import json

import click
import pkg_resources

from . import content
from . import transformer


def logging_config():
    pathname = os.path.join("data", "logging_config.json")

    return pkg_resources.resource_string(__name__, pathname)


# parser = argparse.ArgumentParser(
#     description="Convert a Phenix index.idx.xml file to a LoadData .csv")
# parser.add_argument(
#     "--search-subdirectories", action="store_true",
#     dest="search_subdirectories",
#     help="Look for image files in the index-directory and subdirectories")
# parser.add_argument("--index-file", type=check_file_arg,
#                     dest="index_file",
#                     help="The Phenix index XML metadata file")
# parser.add_argument(
#     "--index-directory", type=check_dir_arg,
#     dest="index_directory",
#     default=os.path.curdir,
#     help="The directory containing the index file and images")
# parser.add_argument(
#     "config_file", type=check_file_arg,
#     help="The config.yaml file that chooses channels and"
#          " metadata for the CSV")
# parser.add_argument(
#     "output_csv",
#     help="The name of the LoadData .csv file to be created")

index_directory_help = """
directory containing the index file and images
"""

index_file_help = """
the Phenix index XML metadata file
"""

search_subdirectories_help = """
Look for image files in the index-directory and subdirectories
"""


@click.command()
@click.argument("configuration", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--index-directory", default=os.path.curdir, help=index_directory_help, type=click.Path(exists=True))
@click.option("--index-file", help=index_file_help, type=click.Path(exists=True))
@click.option("--search-subdirectories", help=search_subdirectories_help, is_flag=True)
def main():
    logging.config.dictConfig(json.load(logging_config()))

    options = transformer.parse_args()
    channels, metadata = transformer.load_config(options.config_file)

    # Strip spaces because XML parser is broken
    channels = dict([(str(k).replace(" ", ""), v) for (k, v) in channels.items()])

    if not options.index_file:
        options.index_file = os.path.join(options.index_directory, "Index.idx.xml")

    handler = content.Handler()

    xml.sax.parse(options.index_file, handler)

    images = handler.root.images.images
    plates = handler.root.plates.plates
    wells = handler.root.wells.wells

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

        transformer.write_csv(writer, images, plates, wells, channels, metadata, paths)
