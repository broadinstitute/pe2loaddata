"""append_illum_cols - Append columns corresponding to illumination functions to a LoadData .csv

"""
import argparse
import csv
import os
import sys
import yaml

           
def check_file_arg(arg):
    '''Make sure the argument is a path to a file'''
    if not os.path.isfile(arg):
        raise argparse.ArgumentTypeError(
            "%s is not a path to an existing file" % arg)
    return arg

def check_dir_arg(arg):
    '''Make sure the argument is a path to an existing directory'''
    if not os.path.isdir(arg):
        raise argparse.ArgumentTypeError(
            "%s is not a path to an existing directory" % arg)
    return arg

 def parse_args():
    parser = argparse.ArgumentParser(
        description = "Append columns corresponding to illumination "
        "functions to a LoadData .csv")

    parser.add_argument("--plate-id",
                        dest = "plate_id",
                        help = "Plate ID")
    parser.add_argument(
        "--illum-directory", type=check_dir_arg,
        dest = "illum_directory",
        help = "The directory containing the illumination functions")
    parser.add_argument(
        "config_file", type = check_file_arg,
        help = "The config.yaml file that chooses channels and"
        " metadata for the CSV")
    parser.add_argument(
        "output_csv", type = check_file_arg,
        help = "The name of the LoadData .csv file to be manipulated")
    return parser.parse_args()

def load_config(config_file):
    '''Load the configuration from config.yaml'''
    with open(config_file, "r") as fd:
        config = yaml.load(fd)
    if isinstance(config, list):
        config = config[0]
    illum_channels = config['illum_channels']
    return channels, metadata
    
def main():
    options = parse_args()
    channels, metadata = load_config(options.config_file)

    # change this to a proper temporary file
    with open(options.output_csv+".tmp", "wb") as fd:
        writer = csv.writer(fd)
        write_csv(writer, illum_channels, options.illum_directory, options.plate_id)

def write_csv(writer, illum_channels, illum_directory, plate_id):
    header = sum([["_".join((prefix, illum_channels[channel])) for prefix in 
                   "FileName", "PathName"]
                   for channel in sorted(illum_channels.keys())], [])
    writer.writerow(header)
    row = sum([["_".join((prefix, illum_channels[channel])) for prefix in 
                   "FileName", "PathName"]
                   for channel in sorted(illum_channels.keys())], [])
    writer.writerow(row)

    #SQ00015201_IllumAGP.mat

                
if __name__ == "__main__":
    main()
