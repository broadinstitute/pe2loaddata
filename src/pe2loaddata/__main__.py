import csv
import os
import shutil
import tempfile
import xml.sax

import click

from . import content
from . import transformer
from . import append_illum_cols

index_directory_help = """
directory containing the index file and images. If on s3, use full s3 URI, starting with 's3://'
"""

index_file_help = """
the Phenix index XML metadata file. If on s3, use full s3 URI, starting with 's3://'
"""

search_subdirectories_help = """
Look for image files in the index-directory and subdirectories. Default is false; set to true if files are on s3.
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


def headless(
    configuration,
    output,
    index_directory=False,
    index_file=False,
    search_subdirectories=False,
    illum_only=False,
    illum=False,
    illum_directory=False,
    plate_id=False,
    illum_filetype='.npy',
    illum_output=False,
    sub_string_out="",
    sub_string_in="",
):
    channels, metadata = transformer.load_config(configuration)

    output_path = os.path.dirname(output)
    if not output_path == "":
        if not os.path.exists(output_path):
            os.makedirs(output_path)  

    # Strip spaces because XML parser is broken
    channels = dict([(str(k).replace(" ", ""), v) for (k, v) in channels.items()])

    if not index_file:
        index_file = os.path.join(index_directory, "Index.idx.xml")

    if "s3" in index_file:
        remote = True
        if not index_directory:
            print(
                "You must also set the --index_directory to use an index_file on S3."
            )
            return
        import boto3
        import botocore

        s3 = boto3.client("s3")
        # Download index file to output directory
        bucket, index_file_key = index_file.split(f"s3://")[1].split("/",1)
        index_file = output_path + "/Index.idx.xml"
        with open(index_file, "wb") as f:
            try:
                s3.download_fileobj(bucket, index_file_key, f)
            except botocore.exceptions.ClientError as error:
                print(
                    "Can't download the xml file. Check file location and permissions."
                )
                print(f"Looking for index_file at {index_file_key}")
                return

    handler = content.Handler()

    xml.sax.parse(index_file, handler)

    images = handler.root.images.images
    plates = handler.root.plates.plates
    wells = handler.root.wells.wells

    paths = {}  

    if not illum_only:
        if search_subdirectories:
            if remote:
                # Create paths dictionary
                index_directory_key = index_directory.split(f"s3://{bucket}/")[1]
                paginator = s3.get_paginator("list_objects_v2")
                pages = paginator.paginate(Bucket=bucket, Prefix=index_directory_key)
                try:
                    for page in pages:
                        for x in page["Contents"]:
                            fullpath = x["Key"]
                            path, filename = fullpath.rsplit("/", 1)
                            if filename.endswith(".tiff"):
                                paths[filename] = path
                except KeyError:
                    print("Listing files in s3 directory failed.")
                    return
                os.remove(index_file)
            else:
                for dir_root, directories, filenames in os.walk(index_directory):
                    for filename in filenames:
                        if filename.endswith(".tiff"):
                            paths[filename] = dir_root
        else:
            for filename in os.listdir(index_directory):
                paths[filename] = index_directory

        with open(output, "w") as fd:
            writer = csv.writer(fd, lineterminator="\n")

            transformer.write_csv(
                writer,
                images,
                plates,
                wells,
                channels,
                metadata,
                paths,
                sub_string_out,
                sub_string_in,
            )

    if illum_only or illum:
        if not all([illum_directory, plate_id, illum_output]):
            print(
                "You must set the --illum-directory, --plate-id, and --illum-output flags when using the illum options in pe2loaddata"
            )

        else:

        
            illum_output_path = os.path.dirname(illum_output)
            if not illum_output_path == "":
                if not os.path.exists(illum_output_path):
                    os.makedirs(illum_output_path)

            with open(output, "r") as fd:
                nrows = sum(1 for _ in fd) - 1

            tmpdir = tempfile.mkdtemp()

            with open(os.path.join(tmpdir, "illum.csv"), "w") as fd:
                illumwriter = csv.writer(fd, lineterminator="\n")
                append_illum_cols.write_csv(
                    illumwriter,
                    channels,
                    illum_directory,
                    plate_id,
                    nrows,
                    illum_filetype,
                    sub_string_out,
                    sub_string_in,
                )

            os.system(
                'paste -d "," {} {} > {}'.format(
                    output, os.path.join(tmpdir, "illum.csv"), illum_output
                )
            )

            shutil.rmtree(tmpdir)



@click.command()
@click.argument("configuration", type=click.Path(exists=True, dir_okay=False))
@click.argument("output", type=click.Path(dir_okay=False))
@click.option(
    "--index-directory",
    default=os.path.curdir,
    help=index_directory_help,
    type=click.Path(exists=True),
)
@click.option(
    "--index-file", help=index_file_help, type=click.Path(exists=True, dir_okay=False)
)
@click.option("--search-subdirectories", help=search_subdirectories_help, is_flag=True)
@click.option("--illum-only", help=illum_only_help, default=False, is_flag=True)
@click.option("--illum/--no-illum", help=illum_help, default=False)
@click.option(
    "--illum-directory",
    default=os.path.curdir,
    help=illum_directory_help,
    type=click.Path(exists=False),
)
@click.option("--plate-id", help="Plate ID", type=click.STRING)
@click.option(
    "--illum-filetype", help=illum_filetype_help, default=".npy", type=click.STRING
)
@click.option("--illum-output", help=illum_output_help, type=click.Path(dir_okay=False))
@click.option(
    "--sub-string-out",
    help="A part of the row (typically a path) you want substituted by sub-string-in",
    type=click.STRING,
    default="",
)
@click.option(
    "--sub-string-in",
    help="A part of the row (typically a path) you want substituted instead of sub-string-out",
    type=click.STRING,
    default="",
)
def main(
    configuration,
    output,
    index_directory,
    index_file,
    search_subdirectories,
    illum_only,
    illum,
    illum_directory,
    plate_id,
    illum_filetype,
    illum_output,
    sub_string_out,
    sub_string_in,
):
    headless(
        configuration,
        output,
        index_directory,
        index_file,
        search_subdirectories,
        illum_only,
        illum,
        illum_directory,
        plate_id,
        illum_filetype,
        illum_output,
        sub_string_out,
        sub_string_in,
    )

