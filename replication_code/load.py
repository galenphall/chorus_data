import pickle

import pandas as pd


def positions(cache=True):
    if cache:
        # Save the positions in RAM
        if not hasattr(positions, 'positions'):
            positions.positions = pd.read_parquet('data/positions.parquet')
        return positions.positions
    else:
        return pd.read_parquet('data/positions.parquet')


def bills(cache=True):
    if cache:
        # Save the bills in RAM
        if not hasattr(bills, 'bills'):
            bills.bills = pd.read_parquet('data/bills.parquet')
        return bills.bills
    else:
        return pd.read_parquet('data/bills.parquet')


def clients(cache=True):
    if cache:
        # Save the clients in RAM
        if not hasattr(clients, 'clients'):
            clients.clients = pd.read_parquet('data/clients.parquet')
        return clients.clients
    else:
        return pd.read_parquet('data/clients.parquet')


def blockstates(cache=True):
    def _blockstate(state, record_type):
        return pickle.load(
            open(f"data/hbsbm/{state}_{record_type}_corrected_categorical_blockstate.pkl", 'rb'))
    def _get_all_blockstates():
        return {
            (state, record_type): _blockstate(state, record_type)
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

    if cache:
        # Save the blockstates in RAM
        if not hasattr(blockstates, 'blockstates'):
            blockstates.blockstates = _get_all_blockstates()
        return blockstates.blockstates
    else:
        return _get_all_blockstates()

def block_assignments(cache=True):
    # load the block assignments (data/block_assignments.csv)
    if cache:
        # Save the block assignments in RAM
        if not hasattr(block_assignments, 'block_assignments'):
            block_assignments.block_assignments = pd.read_csv('data/block_assignments.csv')
        return block_assignments.block_assignments
    else:
        return pd.read_csv('data/block_assignments.csv')
