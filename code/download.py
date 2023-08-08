# Download data from the SPPQ dataverse: https://dataverse.unc.edu/dataverse/sppq
import os
import pathlib

def download_from_dataverse():

    # if the data directory doesn't exist, create it
    path = pathlib.Path('data')
    path.mkdir(exist_ok=True)

    # download the data using wget
    os.system('wget -r -np -nH --cut-dirs=3 -R index.html '
              'https://dataverse.unc.edu/dataset.xhtml?persistentId=doi:10.15139/S3/RPU1QP, -P data')

def download_from_gdrive():
    import gdown

    # if not in the chorus_data directory, change to there
    if not os.getcwd().endswith('chorus_data'):
        os.chdir('chorus_data')

    ## Load the dataset from the public Google Drive folder
    ## This is the same dataset used in the paper
    drive_url = 'https://drive.google.com/drive/folders/1JLxwurbx0ys4DUDB2o-WCtWWsjisVi8L?usp=sharing'

    # Download the contents of the folder at the drive_url to the /data folder
    path = pathlib.Path('data')
    path.mkdir(exist_ok=True)

    gdown.download_folder(drive_url, output='data', quiet=True)