import csv
import os
import xml.sax

import click

from . import content
from . import transformer
from . import append_illum_cols

index_directory_help = """
directory containing the index file and images
"""

index_file_help = """
the Phenix index XML metadata file
"""

search_subdirectories_help = """
Look for image files in the index-directory and subdirectories
"""

illum_only_help = """
Run only the step to append illum columns to an existing file. The "output" CSV will be used instead as input, and you will need to pass --illum-directory and --plate-id, and --illum_output.
"""


illum_help = """
Run both the main pe2loaddata function and the append_illum function. Default is false; if true you need to pass --illum-directory, --plate_id, and --illum_output.
"""

illum_directory_help = """
directory where illumination correction images are or will be
"""

illum_filetype_help = """
The file type of the illum files- in CP2.X, this should be '.mat', in CP3.X or 4.X '.npy'
"""

illum_output_help = """
The destination file for the illum output if both pe2loaddata and append illum are being run
"""

@click.command()
@click.argument("configuration", type=click.Path(exists=True, dir_okay=False))
@click.argument("output", type=click.Path(dir_okay=False))
@click.option("--index-directory", default=os.path.curdir, help=index_directory_help, type=click.Path(exists=True))
@click.option("--index-file", help=index_file_help, type=click.Path(exists=True, dir_okay=False))
@click.option("--search-subdirectories", help=search_subdirectories_help, is_flag=True)
@click.option("--illum-only",help=illum_only_help, default=False, is_flag=True)
@click.option("--illum/--no-illum",help=illum_help, default=False)
@click.option("--illum-directory", default=os.path.curdir, help=illum_directory_help, type=click.Path(exists=False))
@click.option("--plate-id", help="Plate ID", type=click.STRING)
@click.option("--illum-filetype", help=illum_filetype_help, default='.npy', type=click.STRING)
@click.option("--illum-output", help=illum_output_help, type=click.Path(dir_okay=False))
def main(configuration, output, index_directory, index_file, search_subdirectories, illum_only, illum, illum_directory, plate_id, illum_filetype, illum_output):
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

    if not illum_only:
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

    if illum_only or illum:
        if not all([illum_directory,plate_id,illum_output]):
            print("You must set the --illum-directory, --plate-id, and --illum-output flags when using the illum options in pe2loaddata")

        else:
            
            with open(output,'r') as fd:
                nrows = sum(1 for _ in fd) - 1

            with open(illum_output, 'w') as fd:
                illumwriter = csv.writer(fd, lineterminator='\n')
                append_illum_cols.write_csv(illumwriter, channels, illum_directory, plate_id, nrows, illum_filetype)

