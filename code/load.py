import pickle

import pandas as pd


def positions():
    return pd.read_parquet('data/positions.parquet')


def bills():
    return pd.read_parquet('data/bills.parquet')


def clients():
    return pd.read_parquet('data/clients.parquet')


def blockstates():
    return {
        (state, record_type): pickle.load(
            open(f"data/hbsbm/{state}_{record_type}_corrected_categorical_blockstate.pkl", 'rb'))
        for state, record_type in [
            ('MA', 'lobbying'),
            ('CO', 'lobbying'),
            ('TX', 'testimony'),
            ('IA', 'lobbying'),
            ('MT', 'lobbying'),
            ('NE', 'lobbying'),
            ('WI', 'lobbying'),
            ('CO', 'testimony'),
            ('MT', 'testimony'),
            ('AZ', 'testimony'),
            ('MO', 'testimony'),
            ('OH', 'testimony'),
            ('FL', 'testimony'),
            ('NJ', 'lobbying'),
            ('IL', 'testimony'),
            ('MD', 'testimony'),
            ('KS', 'testimony'),
            ('SD', 'testimony'),
            ('RI', 'lobbying'),
        ]
    }
