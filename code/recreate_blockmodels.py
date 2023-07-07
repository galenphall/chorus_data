"""
Code to rerun all blockmodeling for each state and record type. Note that for the resultant blockmodels to be used for
replication, the blockmodeling must be run with the same parameters as in the paper (deg_corr=True, layers=False,
overlap=False). Additionally, the saved blockmodels must be renamed to match the naming convention used in the paper:
    {region}_{record_type}_{corrected}_{categorical}_blockmodel.pkl

"""
