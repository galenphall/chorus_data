![](info/CHORUS logo.png)

# Replication Materials
This repository contains the code and data used in the paper "CHORUS: A new dataset of state interest group policy positions in the United States," forthcoming in _State Politics & Policy Quarterly_.
If you use our code and/or data, please cite the paper as:

> Hall, Galen, Joshua Basseches, Rebecca Bromley-Trujillo, and Trevor Culhane. 2023. "CHORUS: A new dataset of state interest group policy positions in the United States." _State Politics & Policy Quarterly_. Forthcoming 2023.

## Data
The dataset used in the related paper is available online in the SPPQ Dataverse: https://dataverse.unc.edu/dataverse/sppq. To download it locally, run the `code/download.py` file.

_Note that we will maintain updated versions of this dataset at a different location._ For replicating the results in the paper, please use the version of the dataset available in the SPPQ Dataverse.

### File structure
- `data/`: Contains the data used in the paper.
- `data/positions.parquet`: The positions recorded in testimony and lobbying records.
- `data/bills.parquet`: The bills on which positions were recorded, merged with data from LegiScan and the National Conference of State Legislatures for the states in CHORUS.
- `data/clients.parquet`: The organizations that recorded positions on bills in CHORUS.
- `data/block_assignments.parquet`: The block assignments for each organization in each state, from our hierarchical bayesian stochastic block model.
- `data/{IL, TX, MA, CO}_network_figure_clusters_named.xlsx`: Data used to create the network figures in the paper, with the clusters named by the authors.
- `data/hbsbm/{state}_{record_type}_corrected_categorical_blockstate.pkl`: This folder contains `pickle` (`".pkl"`) files for each `BlockModel` object generated using the data corresponding to a unique `{state, record_type}` combination from `positions.parquet` (for example, one file contains the blockmodel for the `testimony` records in `Arizona`). The `corrected` in the filename indicates that the blockmodel incorporated degree correction, and the `categorical` indicates that the blockmodel used categorical edge covariates as opposed to the `layered` model.

## Code
The python code used to generate the data and figures presented in the paper is available in the `code` folder. Code used to create the CHORUS dataset is available for review upon reasonable request.

Files:
- `download.py`: Downloads the data from the SPPQ Dataverse.
- `load.py`: Loads the data into memory as pandas dataframes.
- `figures.py`: Functions to generate the figures presented in the paper.
- `utils.py`: Utility functions for data analysis and plotting.
- `hbsbm.py` : Functions to create the hierarchical bayesian stochastic block models. When recreating results from scratch using `run_all_blockmodels_from_scratch()`, note that since the blockmodels are stochastic, the results will not be identical to those presented in the paper.
- `main.py`: Main file to run the code.

## Figures
The figures presented in the paper are available in the `figures` folder. The code used to generate them is available in the `code/figures.py` file. Note that the figures in the paper have been edited for clarity and aesthetics.

## Requirements
The code was written in Python 3.10 Most required packages are listed in `requirements.txt`. To install them, run the following command in the terminal:
```bash
pip install -r requirements.txt.
```
The hbsbm code also requires the `graph-tool` package, which can be installed via Conda but is not available on PyPI. To install it, follow the instructions [on the graph-tool website](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions).

## License
This project is licensed under the MIT License - see the [LICENSE.md](info/LICENSE.md) file for details.

## Contact
For questions or comments, please contact Galen Hall at
<galen.p.hall [at] gmail.com>.

## Acknowledgments
This project was supported with funding from the Climate Social Science Network (CSSN); see https://cssn.org for more information. We thank the CSSN for their support.

The blockmodeling code is based on the [hbsbm](http://git.skewed.de/count0/hbsbm) package by Tiago Peixoto.

The authors are responsible for all errors.
