"""pe2loaddata - Convert Phenix index.idx.xml file into a .CSV for LoadData

The YAML syntax is:

channels:
   DNA: Hoechst
   GFP: Phalloidin

metadata:
   PositionX=SiteXPosition
   PositionY=SiteYPosition
"""
import argparse
import logging
import logging.config
import os
from os import PathLike
from typing import Union, Any

import yaml


def check_file_arg(arg: Union[bytes, str, PathLike]) -> Union[bytes, str, PathLike]:
    """Make sure the argument is a path to a file"""
    if not os.path.isfile(arg):
        raise argparse.ArgumentTypeError("%s is not a path to an existing file" % arg)

    return arg


def check_dir_arg(arg: Union[bytes, str, PathLike]) -> Union[bytes, str, PathLike]:
    """Make sure the argument is a path to an existing directory"""
    if not os.path.isdir(arg):
        raise argparse.ArgumentTypeError("%s is not a path to an existing directory" % arg)

    return arg


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a Phenix index.idx.xml file to a LoadData .csv"
    )

    parser.add_argument(
        "--search-subdirectories",
        action="store_true",
        dest="search_subdirectories",
        help="Look for image files in the index-directory and subdirectories"
    )

    parser.add_argument(
        "--index-file",
        type=check_file_arg,
        dest="index_file",
        help="The Phenix index XML metadata file"
    )

    parser.add_argument(
        "--index-directory",
        type=check_dir_arg,
        dest="index_directory",
        default=os.path.curdir,
        help="The directory containing the index file and images"
    )

    parser.add_argument(
        "config_file",
        type=check_file_arg,
        help="The config.yaml file that chooses channels and metadata for the CSV"
    )

    parser.add_argument(
        "output_csv",
        help="The name of the LoadData .csv file to be created"
    )

    return parser.parse_args()


def load_config(config_file: Union[bytes, str, PathLike]) -> (Any, Any):
    """Load the configuration from config.yaml"""
    with open(config_file, "r") as fd:
        config = yaml.load(fd, Loader=yaml.BaseLoader)

    if isinstance(config, list):
        config = config[0]

    channels = config['channels']

    metadata = config.get('metadata', {})

    return channels, metadata

def metadata_adjust_image(image, maps, metadata):
    if image.channel_name:
        return image
    else:
        image.channel_name = maps[str(image.channel_id)]['ChannelName'].replace(" ","")
        for key in sorted(metadata.keys()):
            if key not in image.metadata.keys():
                image.metadata[key] = maps[str(image.channel_id)][key]
        return image

def make_row_metadata(dict_of_images, channels, requested_metadata):
    final_metadata = {}
    temp_metadata = {}
    for channel in channels.keys():
        image = dict_of_images[channel]
        for key in requested_metadata:
            if key not in temp_metadata:
                temp_metadata[key] = { channel: image.metadata[key]}
            else:
                temp_metadata[key][channel] = image.metadata[key]
    for k,v in temp_metadata.items():
        all_values = list(set([channelval for channel, channelval in v.items()]))
        if len(all_values) == 1:
            final_metadata[k] = all_values[0]
        else:
            for channel in channels.keys():
                final_metadata[f"{k}_{channels[channel]}"] = v[channel]
    return final_metadata

def write_csv(writer, images, plates, wells, maps, channels, metadata, paths, sub_string_out='', sub_string_in=''):
    header = sum([["_".join((prefix, channels[channel])) for prefix in ["FileName", "PathName"]] for channel in sorted(channels.keys())], [])

    header += ["Metadata_Plate", "Metadata_Well", "Metadata_Site"]

    #we need to actually process one well to figure out what's the metadata to return
    sample_well = wells[list(wells.keys())[0]]
    sample_well_images = {}
    for image_id in sample_well.image_ids:
        image = metadata_adjust_image(images[image_id], maps, metadata)
        sample_well_images[image.channel_name] = image

    adjusted_metadata = make_row_metadata(sample_well_images, channels, sorted(metadata.keys()))

    header += ["_".join(("Metadata", key)) for key in adjusted_metadata]

    writer.writerow(header)

    for plate_name in sorted(plates):
        plate = plates[plate_name]

        for well_id in plate.well_ids:
            well = wells[well_id]

            fields = {}

            well_name = well.well_name

            for image_id in well.image_ids:
                try:
                    image = metadata_adjust_image(images[image_id], maps, metadata)

                    # For simplifying the code, field_id is defined as the combination of
                    # FieldID and PlaneID. Later, PlaneID is stripped out when actually
                    # writing out field_id.
                    field_id = '%02d-%02d' % (int(image.metadata["FieldID"]), int(image.metadata.get("PlaneID", 1)))

                    channel = image.channel_name

                    assert channel in channels

                    if field_id not in fields:
                        fields[field_id] = {channel: image}
                    else:
                        fields[field_id][channel] = image
                except Exception as e:
                    print(e)

            for field in sorted(fields):
                d = fields[field]
                row = []

                for channel in sorted(channels.keys()):
                    try:
                        image = d[channel]

                        file_name = image.metadata["URL"]

                        row += [file_name, paths[file_name]]
                    except Exception as e:
                        logging.debug("Channel = {}; Field = {}; Plate = {}".format(channel, field, plate_name))

                        print(e)

                        row = []

                        break

                if not row:
                    continue

                # strip out the PlaneID from field before writing the row
                row += [plate_name, well_name, str(int(field[:2]))]

                adjusted_metadata = make_row_metadata(d, channels, sorted(metadata.keys()))

                for _, value in adjusted_metadata.items():
                    row.append(value)

                if sub_string_in != '' and sub_string_out != '':
                    row = [x.replace(sub_string_out,sub_string_in) for x in row]

                writer.writerow(row)
