import pytest

@pytest.fixture(scope="module",
    params=[
        (
            'tests/data/Version1/images/',
            'tests/data/Version1/images/Index.idx.xml',
            'tests/data/Version1/config_v1.yml', 
            'tests/data/Version1/load_data_version1.csv',
            {
                "488 long": "OrigRNA",
                "Alexa 488": "OrigER",
                "Alexa 568": "OrigAGP",
                "Alexa 647": "OrigMito",
                "HOECHST 33342": "OrigDNA",
                "Brightfield": "OrigBrightfield"
                },
        ),
        (
            'tests/data/Version5/images/',
            'tests/data/Version5/images/Index.idx.xml',
            'tests/data/Version5/config_v5.yml', 
            'tests/data/Version5/load_data_version5.csv',
             {
                "Brightfield high": "OrigBrightfield",
                "Alexa 568": "OrigAGP",
                "Alexa 647": "OrigMito",
                "Alexa 488": "OrigER",
                "488 650": "OrigRNA",
                "Digital Phase Contrast": "OrigDPC"
            },
        ),
        (
            'tests/data/Version7/images/',
            'tests/data/Version7/images/Index.xml',
            'tests/data/Version7/config_v7.yml', 
            'tests/data/Version7/load_data_version7.csv',
                {
                    "HOECHST 33342": "OrigDNA",
                    "Alexa 568": "OrigAGP",
                    "Alexa 647": "OrigMito",
                    "Alexa 488": "OrigER",
                    "Alexa 488 Em 650": "OrigRNA",
                    "Brightfield": "OrigBrightfield",
                    "405ex, 570-630-em)": "OrigActin"
                },
        ),
    ],  
    ids=["v1", "v5", "v7"],)
def test_files(request):
    index_directory, index_file, config_file, output_file, expected_channels = request.param
    test_dict = {'index_directory':index_directory,'index_file':index_file,
                 'config_file':config_file,'output_file':output_file,
                 'expected_channels':expected_channels}
    return test_dict
