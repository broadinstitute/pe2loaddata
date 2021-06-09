"""append_illum_cols - Append columns corresponding to illumination functions to a LoadData .csv

"""
import argparse
import csv
import os
import shutil
import tempfile
from os import PathLike
from typing import Union, Any
import yaml


def check_file_arg(arg: Union[bytes, str, PathLike]) -> Union[bytes, str, PathLike]:
    """Make sure the argument is a path to a file"""
    if not os.path.isfile(arg):
        raise argparse.ArgumentTypeError(
            "%s is not a path to an existing file" % arg)
    return arg


def check_dir_arg(arg: Union[bytes, str, PathLike]) -> Union[bytes, str, PathLike]:
    """Make sure the argument is a path to an existing directory"""
    if not os.path.isdir(arg):
        raise argparse.ArgumentTypeError(
            "%s is not a path to an existing directory" % arg)
    return arg


def parse_args():
    parser = argparse.ArgumentParser(
        description="Append columns corresponding to illumination "
                    "functions to a LoadData .csv")

    parser.add_argument("--plate-id",
                        dest="plate_id",
                        help="Plate ID")

    parser.add_argument(
        "--illum-directory", type=check_dir_arg,
        dest="illum_directory",
        help="The directory containing the illumination functions")

    parser.add_argument(
        "config_file", type=check_file_arg,
        help="The config.yaml file that chooses channels and"
             " metadata for the CSV")

    parser.add_argument(
        "--illum_filetype", default='.npy', dest='illum_filetype',
        help="The file type of the illum files- in CP2.X, this should be '.mat', in CP3.X '.npy'")

    parser.add_argument(
        "input_csv", type=check_file_arg,
        help="The name of the LoadData .csv file to be manipulated")

    parser.add_argument(
        "output_csv",
        help="The name of the LoadData .csv file to be created after appending")

    return parser.parse_args()


def load_config(config_file: Union[bytes, str, PathLike]) -> (Any, Any):
    """Load the configuration from config.yaml"""
    with open(config_file, "r") as fd:
        config = yaml.load(fd, Loader=yaml.BaseLoader)

    # if isinstance(config, list):
    #     config = config[0]

    channels = config['channels']

    return channels


def main():

    options = parse_args()
    channels = load_config(options.config_file)
    nrows = sum(1 for _ in open(options.input_csv)) - 1

    tmpdir = tempfile.mkdtemp()

    with open(os.path.join(tmpdir, 'illum.csv'), 'w') as fd:
        writer = csv.writer(fd, lineterminator='\n')

        write_csv(writer, channels, options.illum_directory, options.plate_id, nrows, options.illum_filetype)



    os.system('paste -d "," {} {} > {}'.format(options.input_csv,
                                               os.path.join(tmpdir, 'illum.csv'),
                                               options.output_csv
                                               ))


    shutil.rmtree(tmpdir)


def write_csv(writer, channels, illum_directory, plate_id, nrows, illum_filetype, sub_string_out='', sub_string_in=''):
    header = sum(
        [["_Illum".join((prefix, channel.replace("Orig", ""))) for prefix in ["FileName", "PathName"]] for channel in
         sorted(channels.values())], [])

    writer.writerow(header)

    row = sum([[plate_id + '_Illum' + channel.replace("Orig", "") + illum_filetype, illum_directory] for
               channel in sorted(channels.values())], [])
    if sub_string_in != '' and sub_string_out != '':
        row = [x.replace(sub_string_out,sub_string_in) for x in row]
    writer.writerows([row] * nrows)


if __name__ == "__main__":
    main()
