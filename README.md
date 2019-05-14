# pe2loaddata
Script to parse a Phenix metadata XML file and generate a .CSV for CellProfiler's loaddata module

To run:

    python pe2loaddata.py --index-directory=<index-directory> config.yml output.csv

where <index-directory> is the directory containing the Index.idx.xml file and the images, config.yml is the LoadData configuration file and output.csv is the CSV that will be generated.

The config.yml file lets you name the channels you want to save and lets you pull metadata out of the image. An example:

    channels:
        HOECHST 33342: OrigDNA
        Alexa 568: OrigAGP
        Alexa 647: OrigMito
        Alexa 488: OrigER
        488 long: OrigRNA
    metadata:
        Row: Row
        Col: Col
        FieldID: FieldID
        PlaneID: PlaneID
        ChannelID: ChannelID
        ChannelName: ChannelName
        ImageResolutionX: ImageResolutionX
        ImageResolutionY: ImageResolutionY
        ImageSizeX: ImageSizeX
        ImageSizeY: ImageSizeY
        BinningX: BinningX
        BinningY: BinningY
        MaxIntensity: MaxIntensity
        PositionX: PositionX
        PositionY: PositionY
        PositionZ: PositionZ
        AbsPositionZ: AbsPositionZ
        AbsTime: AbsTime
        MainExcitationWavelength: MainExcitationWavelength
        MainEmissionWavelength: MainEmissionWavelength
        ObjectiveMagnification: ObjectiveMagnification
        ObjectiveNA: ObjectiveNA
        ExposureTime: ExposureTime

In the above example, "HOECHST 33342" is the label for the DNA channel and
if you load the .csv file in LoadData, you will get an image named "DNA" in
your image set.

The metadata section selects items out of the image metadata and allows
you to rename them as metadata. In addition, pe2loaddata automatically
populates the plate, well and site metadata entriess.

pe2loaddata now supports experiments with multiple planes per field as long as the `PlaneID` field 
has been set in the config file.

As of 2019-05-14, running `append_illum_cols.py` will create CSVs where the illumination file name 
ends in `.npy`, not `.mat`.  If you wish to continue CellProfiler 2.X compatibility, you can 
explicitly pass `.mat` as an argument to `append_illum_cols.py`.    
