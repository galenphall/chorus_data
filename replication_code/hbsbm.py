import datetime
import json
import pickle
from collections import defaultdict

import graph_tool.all as gt
import networkx as nx
import numpy as np
import pandas as pd
import tqdm


def get_bipartite_graph(bipartite_adj_matrix: pd.DataFrame):
    """
    Construct a bipartite graph representing positions data from an adjacency matrix
    This replication_code is adapted from the sbmtm model replication_code: https://github.com/martingerlach/hSBM_Topicmodel
    :param bipartite_adj_matrix: the adjacency matrix
    :return: a bipartite graph-tool graph
    """
    # Construct edgelist; for now, keep only positive and negative positions
    E_combo = bipartite_adj_matrix[~bipartite_adj_matrix.isna()].stack()
    E_combo = E_combo.reset_index(drop=False)
    E_combo.columns = ['source', 'target', 'weight']
    E_combo = E_combo[E_combo.weight.isin([1, -1])]

    g = gt.Graph(directed=False)

    # define node properties
    # name: clients - client_uuid, bills - unified_bill_id
    # kind: clients - 0, bills - 1
    name = g.vp["name"] = g.new_vp("string")
    kind = g.vp["kind"] = g.new_vp("int")
    etype = g.ep["weight"] = g.new_ep("int")

    bills_add = defaultdict(lambda: g.add_vertex())
    clients_add = defaultdict(lambda: g.add_vertex())

    igs = E_combo.source.unique()
    bls = E_combo.target.unique()

    I = len(igs)
    # add all interest groups first
    for i in range(I):
        ig = igs[i]
        d = clients_add[ig]
        name[d] = ig
        kind[d] = 0

    # add all bills
    for i in range(len(bls)):
        bill = bls[i]
        b = bills_add[bill]
        name[b] = bill
        kind[b] = 1

    # add all edges and assign their type = to the numeric position
    for i in tqdm.tqdm(range(len(E_combo))):
        i_client = np.where(igs == E_combo.iloc[i]['source'])[0][0]
        i_bill = np.where(bls == E_combo.iloc[i]['target'])[0][0]
        e = g.add_edge(i_client, I + i_bill)
        etype[e] = E_combo.iloc[i]['weight']

    return g


def remove_redundant_levels(state: gt.BlockState):
    """
    Remove redundant levels from a blockstate
    Taken from sbmtm model replication_code: https://github.com/martingerlach/hSBM_Topicmodel
    :param state: the blockstate
    :return:
    """

    state_tmp = state.copy()
    mdl = state_tmp.entropy()

    L = 0
    for s in state_tmp.levels:
        L += 1
        if s.get_nonempty_B() == 2:
            break
        state_tmp = state_tmp.copy(bs=state_tmp.get_bs()[:L] + [np.zeros(1)])

        mdl_tmp = state_tmp.entropy()
        if mdl_tmp < mdl:  # if the model is better, keep the change
            mdl = 1.0 * mdl_tmp
            state = state_tmp.copy()

    return state


def get_bipartite_adjacency_matrix(positions: pd.DataFrame, k_core: tuple = (5, 5)):
    """
    Construct an adjacency matrix from positions data
    :param positions: the positions dataframe
    :param k_core: the minimum number of clients and bills that must have a position for it to be included in the
        adjacency matrix. Default is (5, 5).
    :return: the adjacency matrix
    """

    selection = positions[positions.client_uuid.notnull()].copy()
    selection = selection[selection.unified_bill_id.notnull()]

    n_client_positions = selection.client_uuid.value_counts()
    n_bill_positions = selection.unified_bill_id.value_counts()

    selection = selection[selection.client_uuid.map(n_client_positions) >= k_core[0]]
    selection = selection[selection.unified_bill_id.map(n_bill_positions) >= k_core[1]]

    A = selection.groupby(['client_uuid', 'unified_bill_id']).position_numeric.sum().unstack()

    A = np.sign(A)

    del selection

    while any(abs(A).sum(0) < k_core[1]) or any(abs(A).sum(1) < k_core[0]):
        A = A.loc[:, abs(A).sum(0) >= k_core[1]]
        A = A.loc[abs(A).sum(1) >= k_core[0], :]

    # Make sure we still have some data
    assert A.shape[0] > 0 and A.shape[1] > 0, "No data left after filtering"

    # Get the largest connected component
    g = nx.from_pandas_adjacency(A)
    giant_component = set(max(nx.connected_components(g), key=len))
    remaining_clients = giant_component & set(A.index)
    remaining_bills = giant_component & set(A.columns)
    A = A.reindex(index=remaining_clients, columns=remaining_bills)
    return A


def save_blockmodel_and_metadata(blockstate, region, record_type, deg_corr, layers, overlap, pmode=None, **kwargs):
    """
    Save a blockmodel and its metadata
    :param blockstate: the blockstate
    :param region: the region (US state)
    :param record_type: the record type
    :param deg_corr: the degree correction parameter
    :param layers: whether the blockmodel has layers
    :param overlap: the overlap parameter
    :param pmode: the PartitionModeState object
    :param kwargs: any additional metadata
    :return:
    """
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    blockmodel_path = f"data/hbsbm/{date_time}"

    metadata = {
        'region': region,
        'record_type': record_type,
        'deg_corr': deg_corr,
        'layers': layers,
        'overlap': overlap,
        **kwargs
    }

    with open(blockmodel_path + '.pkl', 'wb') as f:
        pickle.dump(blockstate, f)

    with open(blockmodel_path + '_metadata.json', 'w') as f:
        json.dump(metadata, f)

    if pmode is not None:
        with open(blockmodel_path + '_pmode.pkl', 'wb') as f:
            pickle.dump(pmode, f)


def estimate_blockmodel(graph, deg_corr: bool, layers: bool, overlap: bool):
    """
    Run a blockmodel on a graph-tool graph with the given parameters
    :param graph:
    :param deg_corr:
    :param layers:
    :param overlap:
    :return:
    """

    if not overlap:
        clabel = graph.vp['kind']
    else:
        clabel = None

    print("Estimating blockstate")
    blockstate = gt.minimize_nested_blockmodel_dl(
        graph,
        state_args=dict(
            base_type=gt.LayeredBlockState,
            clabel=clabel, pclabel=clabel,  # impose hard bipartite constraint
            state_args=dict(ec=graph.ep.weight,
                            layers=layers,
                            deg_corr=deg_corr,
                            overlap=overlap,
                            )),
        multilevel_mcmc_args=dict(verbose=True)
    )

    return blockstate


def refine_blockmodel(blockstate, overlap):
    """
    Refine a blockmodel by annealing and removing redundant levels
    :param blockstate:
    :param overlap:
    :return:
    """
    if overlap:
        print("Running MCMC sweeps...")
        for _ in tqdm.tqdm(range(1000)):  # this should be sufficiently large
            blockstate.multiflip_mcmc_sweep(beta=np.inf, niter=10)
        print("Done.")

    else:
        print("Annealing blockstate...")
        gt.mcmc_anneal(blockstate,
                       beta_range=(1, 10),
                       niter=1000,
                       mcmc_equilibrate_args=dict(force_niter=10),
                       )
        print("Done.")

    return remove_redundant_levels(blockstate)


def get_partition_mode_state(blockstate):
    """
    Get the partition mode blockstate from a blockstate object
    :param blockstate:
    :return:
    """
    bs = []  # partitions

    def collect_partitions(s):
        bs.append(s.get_state())

    # Now we collect 2000 partitions; but the larger this is, the
    # more accurate will be the calculation
    print("Collecting partition modes...")
    gt.mcmc_equilibrate(blockstate, force_niter=1000, mcmc_args=dict(niter=10),
                        callback=collect_partitions)
    # Infer partition modes
    pmode = gt.ModeClusterState(bs, nested=True)

    return pmode


def run_blockmodel_from_scratch(positions: pd.DataFrame, state: str, record_type: str, deg_corr: bool, layers: bool,
                                overlap: bool = False):
    """
    Run a blockmodel from scratch and save it to disk with metadata and partition mode.
    :param positions: subset of the positions dataframe
    :param state: the US state
    :param record_type: 'lobbying' or 'testimony'
    :param deg_corr: whether to use degree correction
    :param layers: whether to use layers or categorical labels
    :param overlap: whether to allow overlappping blocks
    :return:
    """
    selected_positions = positions[(positions.state == state) & (positions.record_type == record_type)]
    adj_matrix = get_bipartite_adjacency_matrix(selected_positions, k_core=(5, 5))
    graph = get_bipartite_graph(adj_matrix)
    blockstate = estimate_blockmodel(graph, deg_corr, layers, overlap)
    blockstate = refine_blockmodel(blockstate, overlap)
    pmode = get_partition_mode_state(blockstate)

    save_blockmodel_and_metadata(blockstate, state, record_type, deg_corr, layers, overlap, pmode=pmode)


def run_all_blockmodels_from_scratch(positions: pd.DataFrame,
                                     deg_corr: bool = True,
                                     layers: bool = False,
                                     overlap: bool = False):
    """
    Run all blockmodels from scratch and save them to disk with metadata and partition mode.
    :param positions: the positions dataframe
    :param deg_corr: see run_blockmodel_from_scratch
    :param layers: see run_blockmodel_from_scratch
    :param overlap: see run_blockmodel_from_scratch
    :return:
    """
    for state, record_type in positions[['state', 'record_type']].value_counts().index.values[::-1]:
        print(f"Running {state} {record_type}")
        run_blockmodel_from_scratch(positions, state, record_type, deg_corr, layers, overlap)
