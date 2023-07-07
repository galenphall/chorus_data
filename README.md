**Replication Materials** for 

Galen Hall, Joshua Basseches, Rebecca Bromley-Trujillo, and Trevor Culhane, "CHORUS: A new dataset of state interest group policy positions in the United States", _State Politics & Policy Quarterly_ (forthcoming 2023).

If you use our code and/or data, please cite the paper as:

```
@article{hall2023chorus,
  title={CHORUS: A new dataset of state interest group policy positions in the United States},
  author={Hall, Galen and Basseches, Joshua and Bromley-Trujillo, Rebecca and Culhane, Trevor},
  journal={State Politics \& Policy Quarterly},
  year={2023},
  publisher={SAGE Publications Sage CA: Los Angeles, CA}
}
```

## Data
The data used in this project is available online in the SPPQ Dataverse: https://dataverse.harvard.edu/dataverse/sppq. To download it locally, run the `code/download.py` file.

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
The code was written in Python 3.10 The required packages are listed in `requirements.txt`. To install them, run the following command in the terminal:
```bash
pip install -r requirements.txt.
```
