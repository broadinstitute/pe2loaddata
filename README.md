# pe2loaddata
Script to parse a Phenix metadata XML file and generate a .CSV for CellProfiler's loaddata module

To run:

    python pe2loaddata.py --index-directory=<index-directory> config.yml output.csv

where <index-directory> is the directory containing the Index.idx.xml file and the images, config.yml is the LoadData configuration file and output.csv is the CSV that will be generated.

The config.yml file lets you name the channels you want to save and lets you pull metadata out of the image. An example:

    channels:
        HOECHST 33342: DNA
        Alexa 568: Actin
        Alexa 647: Golgi
        Alexa 488: Mito

    metadata:
        AbsPositionZ: Z

In the above example, "HOECHST 33342" is the label for the DNA channel and
if you load the .csv file in LoadData, you will get an image named "DNA" in
your image set.

The metadata section selects items out of the image metadata and allows
you to rename them as metadata. In addition, pe2loaddata automatically
populates the plate, well and site metadata entriess.
