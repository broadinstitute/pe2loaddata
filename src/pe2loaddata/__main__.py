import csv
import os
import xml.sax

import click

from . import content
from . import transformer

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
def main(configuration, output, index_directory, index_file, search_subdirectories):
    channels, metadata = transformer.load_config(configuration)

    # Strip spaces because XML parser is broken
    channels = dict([(str(k).replace(" ", ""), v) for (k, v) in channels.items()])

    if not index_file:
        index_file = os.path.join(index_directory, "Index.idx.xml")

    handler = content.Handler()

    xml.sax.parse(index_file, handler)

    images = handler.root.images.images
    plates = handler.root.plates.plates
    wells = handler.root.wells.wells

    paths = {}

    if search_subdirectories:
        for dir_root, directories, filenames in os.walk(index_directory):
            for filename in filenames:
                if filename.endswith(".tiff"):
                    paths[filename] = dir_root
    else:
        for filename in os.listdir(index_directory):
            paths[filename] = index_directory

    with open(output, "w") as fd:
        writer = csv.writer(fd, lineterminator='\n')

        transformer.write_csv(writer, images, plates, wells, channels, metadata, paths)
