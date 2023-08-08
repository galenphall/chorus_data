# This is run from the outer directory, not the replication_code directory, so we need to add the replication_code
# directory to the path.
import pathlib
import sys

sys.path.append('replication_code')

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import normalized_mutual_info_score
from sklearn.naive_bayes import MultinomialNB
import load
from figures import *
from replication_code.utils import CLIENT_ID_COL, BILL_ID_COL


def main():
    currpath: pathlib.Path = pathlib.Path.cwd()

    # if we're inside the replication_code folder, move up one level
    if currpath.name == 'replication_code':
        os.chdir('..')
        currpath = pathlib.Path.cwd()

    # if '/figures' is not in the current directory, add it
    if not (currpath / 'figures').exists():
        (currpath / 'figures').mkdir()

    if not (currpath / 'tables').exists():
        (currpath / 'tables').mkdir()

    if not (currpath / 'data').exists():
        (currpath / 'data').mkdir()

    from hbsbm import get_bipartite_adjacency_matrix

    """Load all position, bill, client data"""
    positions, clients, bills = load.positions(), load.clients(), load.bills()
    blockstates = load.blockstates()

    # make dataframe of block assignments from blockstates
    if not (currpath / 'data/block_assignments.parquet').exists():
        block_assignments = pd.DataFrame()
        for state, record_type in blockstates.keys():
            blockstate = blockstates[(state, record_type)]
            blocks = {level: dict(zip(
                blockstate.g.vp.name,
                blockstate.project_partition(level, 0)
            )) for level in range(len(blockstate.levels))}
            blocks_df = pd.DataFrame(blocks)
            blocks_df['state'] = state
            blocks_df['record_type'] = record_type
            blocks_df.index.name = 'entity_id'
            blocks_df = blocks_df.reset_index(drop=False)

            # add state to entity_id because blockmodels were run separately for each state
            # and did not use unique entity_ids across states
            blocks_df['entity_id'] = blocks_df.state + '_' + blocks_df['entity_id'].astype(str)
            block_assignments = pd.concat([block_assignments, blocks_df], axis=0, ignore_index=True)
        block_assignments.to_parquet('data/block_assignments.parquet', index=False)
    else:
        block_assignments = load.block_assignments()

    """Load Wisconsin data"""
    wi_blockstate = blockstates[('WI', 'lobbying')]
    wi_positions = positions[positions.state == 'WI']

    wi_graph = wi_blockstate.g
    wi_block_levels = pd.DataFrame({
        l: dict(zip(wi_graph.vp.name, wi_blockstate.project_partition(l, 0)))
        for l in range(len(wi_blockstate.levels))
    }).applymap(lambda l: f"wi{l}")
    wi_block_levels.index = 'WI_' + wi_block_levels.index.astype(str)

    wi_clients = clients[clients.state == 'WI'].copy()
    wi_bills = bills[bills.state == 'WI'].copy()

    for level in range(0, len(wi_blockstate.levels)):
        wi_bills[f'block_level_{level}'] = wi_bills[BILL_ID_COL].map(wi_block_levels[level])
        wi_clients[f'block_level_{level}'] = wi_clients[CLIENT_ID_COL].map(wi_block_levels[level])

    ### Tables ###

    """Table 1: Summary statistics"""
    n_positions = positions.groupby(['state', 'record_type']).position_numeric.value_counts().unstack()
    percent_neutral = (n_positions.apply(lambda p: p[0] / sum(p), 1) * 100).round(1)
    avg_per_bill = positions.groupby(['state', 'record_type']).apply(
        lambda p: len(p) / p[BILL_ID_COL].nunique()).round(1)
    years_covered = positions.groupby(['state', 'record_type']).year.apply(lambda y: f"{min(y)}-{max(y)}")

    chamber_map = {
        'S': 'Senate',
        'H': 'House',
        'A': 'Assembly',
        'L': 'Unicameral'
    }

    # extract prefix from bill_id, map to chamber, and then group by state and record_type
    positions['unified_prefix'] = positions[BILL_ID_COL].str.split('_').str[1]

    positions['chamber'] = positions.unified_prefix.str[0].map(chamber_map)
    chambers_covered = positions.groupby(['state', 'record_type']).chamber.apply(
        lambda chambers: sorted({c for c in chambers.unique() if sum(chambers == c) > 100})).map(', '.join)

    table_1 = pd.concat([n_positions, percent_neutral, avg_per_bill, years_covered, chambers_covered], axis=1)
    table_1.columns = ['Support', 'Neutral', 'Oppose', '% Neutral', 'Average positions per bill', 'Years covered',
                       'Chambers covered']
    table_1.index.names = ['State', 'Record Type']
    table_1.to_excel('tables/summary_statistics.xlsx')

    """Table 2: Example block"""
    level_0_block_sizes = wi_clients.drop_duplicates(CLIENT_ID_COL).block_level_0.value_counts()
    highlighted_client_block = level_0_block_sizes.index[0]
    largest_block = wi_clients[wi_clients.block_level_0 == highlighted_client_block]
    table_2 = largest_block.drop_duplicates(CLIENT_ID_COL)
    table_2 = table_2[['client_name', 'ftm_industry']]
    table_2.columns = ['Interest Group', 'Industry']
    table_2.to_excel('tables/wi_example_client_block.xlsx', index=False)

    """Table 3: Words predictive of block membership"""

    def get_bill_block_words(bill_table, level, naivebayesclass=MultinomialNB):
        bill_table = bill_table[bill_table[level].notna()]

        tfidf = TfidfVectorizer()

        X = tfidf.fit_transform(bill_table.title.replace(np.nan, ''))
        y = bill_table[level]

        nb = naivebayesclass()

        nb.fit(X, y)

        bill_category_loadings = pd.DataFrame(
            nb.predict_proba(tfidf.transform(tfidf.get_feature_names_out())),
            index=tfidf.get_feature_names_out(),
            columns=nb.classes_)

        bill_category_loadings = bill_category_loadings.div(bill_category_loadings.sum(0), 1)

        return bill_category_loadings.T

    bill_category_loadings = {level: get_bill_block_words(wi_bills, f'block_level_{level}') for level in
                              range(len(wi_blockstate.levels))}

    level = 3
    top_words = bill_category_loadings[level].apply(lambda r: ', '.join(r.nlargest(5).index.values), 1)
    n_bills = wi_bills[f'block_level_{level}'].value_counts()
    pct_passed = wi_bills.groupby(f'block_level_{level}').apply(
        lambda b: (b.status.isin([4, 5]).sum() / b.status.notna().sum()))

    table_3 = pd.concat([n_bills, pct_passed, top_words], 1)
    table_3.columns = ['N', '% passed', 'top descriptors']
    table_3.to_excel('tables/wi_high_level_bill_categories.xlsx')

    """Table 4 and 5: entropy of bills and clients"""
    # Calculate average entropy for members of each industry

    client_block_level_0 = wi_clients.set_index(CLIENT_ID_COL).block_level_0.to_dict()
    bill_block_level_0 = wi_bills.set_index(BILL_ID_COL).block_level_0.to_dict()
    wi_matrix = wi_positions.pivot_table('position_numeric', CLIENT_ID_COL, BILL_ID_COL,
                                         lambda x: int(any(x.notna())))

    def entropy(x):
        """
        Calculate entropy of a vector of counts
        :param x:
        :return:
        """
        x = np.array(x)
        x = x[x > 0]
        x = x / x.sum()
        return -sum(x * np.log(x))

    bill_client_cts = wi_matrix.groupby(client_block_level_0).sum()
    bill_client_cts = bill_client_cts.loc[:, bill_client_cts.sum(0) > 0]
    bill_entropy = bill_client_cts.apply(entropy).sort_values()[::-1]
    bill_entropy.name = 'bill_entropy'
    bill_entropy_table = wi_bills[wi_bills.legiscan_bill.notna()].set_index(BILL_ID_COL)[['title']].join(
        bill_entropy).dropna()
    bill_entropy_table = bill_entropy_table.sort_values('bill_entropy').drop_duplicates('title')
    pd.concat([bill_entropy_table[::-1][:5], bill_entropy_table[:5]]).to_excel('tables/bill_entropy.xlsx')

    client_bill_cts = wi_matrix.T.groupby(bill_block_level_0).sum()
    client_bill_cts = client_bill_cts.loc[:, client_bill_cts.sum(0) > 0]
    client_entropy = client_bill_cts.apply(entropy).sort_values()[::-1]
    client_entropy.name = 'client_entropy'
    client_entropy_table = wi_clients.drop_duplicates(CLIENT_ID_COL).set_index(CLIENT_ID_COL)[['client_name']].join(
        client_entropy).dropna()
    client_entropy_table = client_entropy_table.sort_values('client_entropy')
    pd.concat([client_entropy_table[::-1][:5], client_entropy_table[:5]]).to_excel('tables/client_entropy.xlsx')


    # Clean up memory
    del bill_client_cts, client_bill_cts, wi_matrix
    del bill_entropy, client_entropy, bill_entropy_table, client_entropy_table
    del bill_category_loadings, top_words, n_bills, pct_passed
    del table_3, table_2, table_1

    ################
    ### Figures ###
    ################

    """Figure 1: Histogram of records per year"""
    records_per_year = positions[
        positions[CLIENT_ID_COL].notna() &
        (positions.year < 2022)].groupby(['record_type', 'year']).position_numeric.count().unstack().T

    fig = figure_1_records_per_year(records_per_year)
    fig.savefig('figures/figure_1_histogram.png', bbox_inches='tight', dpi=300)
    fig.savefig('figures/figure_1_histogram.pdf', bbox_inches='tight')

    """Figure 2: Histogram of records per bill and per client"""
    records_per_bill = positions[[BILL_ID_COL, 'record_type']].value_counts().unstack()
    records_per_bill_hist = records_per_bill.apply(lambda c: 2 ** (np.round(np.log2(c)))).apply(
        lambda c: c.value_counts())
    records_per_client = positions[[CLIENT_ID_COL, 'record_type']].value_counts().unstack()
    records_per_client_hist = records_per_client.apply(lambda c: 2 ** (round(np.log2(c)))).apply(
        lambda c: c.value_counts())

    fig = figure_2_histogram(records_per_bill_hist, records_per_client_hist)
    fig.savefig('figures/figure_2_histogram.png', bbox_inches='tight', dpi=300)
    fig.savefig('figures/figure_2_histogram.pdf', bbox_inches='tight')

    """Figure 3: Wisconsin blockmodel"""
    figure_3_blockmodel(wi_blockstate)
    # this does not return a matplotlib figure, but rather saves a file

    """Figure 4: interest group-level projection of the Wisconsin blockmodel"""
    fig = figure_4_blockmodel_projection(wi_positions, wi_block_levels, wi_clients, block_level=3)
    fig.savefig('figures/figure_4_blockmodel_projection.png', bbox_inches='tight', dpi=300)
    fig.savefig('figures/figure_4_blockmodel_projection.pdf', bbox_inches='tight')

    """Figure 5a: NMI for known and guessed industry labels in the Wisconsin blockmodel for each level of the hierarchy"""
    # Get all clients with known industry labels and block memberships
    known_ftm_sample = wi_clients[
        ~wi_clients.ftm_guessed &
        wi_clients.block_level_0.notna()
        ].drop_duplicates(CLIENT_ID_COL)

    # Get all clients with guessed industry labels and block memberships
    guessed_sample = wi_clients[
        wi_clients.ftm_guessed &
        wi_clients.block_level_0.notna()
        ].drop_duplicates(CLIENT_ID_COL)

    # Compute NMI for each level of the hierarchy between the block memberships and the known and guessed industry labels
    known_nmi = {}
    guessed_nmi = {}
    for l in range(len(wi_blockstate.levels)):
        known_nmi[l] = normalized_mutual_info_score(known_ftm_sample.ftm_industry, known_ftm_sample[f'block_level_{l}'])
        guessed_nmi[l] = normalized_mutual_info_score(guessed_sample.ftm_industry, guessed_sample[f'block_level_{l}'])

    fig, ax = figure_5_nmi_a(known_nmi, known_ftm_sample, guessed_nmi, guessed_sample)
    fig.savefig('figures/figure_5a_industry_nmi.pdf', bbox_inches='tight')
    fig.savefig('figures/figure_5a_industry_nmi.png', bbox_inches='tight', dpi=300)

    """Figure 5b: NMI for known and guessed issue labels in the Wisconsin blockmodel for each level of the hierarchy"""
    # Get all bills with metatopics and block memberships
    wi_bills_sample = wi_bills[
        wi_bills.ncsl_metatopics.apply(lambda x: (x is not None) and (len(x) > 0)) &
        wi_bills.block_level_0.notna()
        ].drop_duplicates(BILL_ID_COL)

    # Get all bills with topics and block memberships
    wi_bills_with_topics = wi_bills[
        wi_bills.ncsl_topics.apply(lambda x: (x is not None) and (len(x) > 0)) &
        wi_bills.block_level_0.notna()
        ].drop_duplicates(BILL_ID_COL)

    topic_nmi = {}
    for l in range(len(wi_blockstate.levels)):
        topic_nmi[l] = normalized_mutual_info_score(wi_bills_with_topics.ncsl_topics.apply(lambda x: x.split(', ')[-1]),
                                                    wi_bills_with_topics[f'block_level_{l}'])

    meta_topic_nmi = {}
    for l in range(len(wi_blockstate.levels)):
        meta_topic_nmi[l] = normalized_mutual_info_score(
            wi_bills_sample.ncsl_metatopics.apply(lambda x: x.split(', ')[0]),
            wi_bills_sample[f'block_level_{l}'])

    fig = figure_5_nmi_b(topic_nmi, wi_bills_with_topics, meta_topic_nmi, wi_bills_sample)
    fig.savefig('figures/figure_5b_topic_nmi.pdf', bbox_inches='tight')
    fig.savefig('figures/figure_5b_topic_nmi.png', bbox_inches='tight', dpi=300)

    """Figure 6: client-level projection of blockstates for lobbying/testimony on energy and climate bills in four 
    states """

    adj_matrices = []
    block_names_list = []

    for region, record_type, level in [
        ('CO', 'lobbying', 1),
        ('TX', 'testimony', 0),
        ('IL', 'testimony', 1),
        ('MA', 'lobbying', 1)]:

        label_column = f'block_level_{level}'

        region_positions = positions[positions.state == region.upper()].copy()

        region_block_assignments = block_assignments[
            (block_assignments.state == region.upper()) & (block_assignments.record_type == record_type)].copy()
        region_block_assignments = region_block_assignments.drop(columns=['state', 'record_type'])
        region_block_assignments = region_block_assignments.set_index('entity_id')

        graph_positions = region_positions[
            region_positions[CLIENT_ID_COL].isin(region_block_assignments.index.values) &
            region_positions.ncsl_metatopics.astype(str).str.contains('energy')
            ]

        adj_matrix = get_bipartite_adjacency_matrix(graph_positions, (5, 3))

        if not os.path.exists(f'data/{region.upper()}_network_figure_clusters_named.csv'):

            region_clients = clients[clients.state == region.upper()].copy()
            region_bills = bills[bills.state == region.upper()].copy()
            n_levels = region_block_assignments.dropna(axis=1).shape[1]

            for l in range(n_levels):
                region_bills[f'block_level_{l}'] = region_bills[BILL_ID_COL].map(region_block_assignments[l])
                region_clients[f'block_level_{l}'] = region_clients[CLIENT_ID_COL].map(region_block_assignments[l])

            block_names = region_clients.set_index(CLIENT_ID_COL)[label_column].astype(str).to_dict()

            n_clients = abs(adj_matrix).groupby(block_names).apply(len)
            block_names = {k: v for k, v in block_names.items() if
                           (k in adj_matrix.index) and (v in n_clients) and (n_clients[v] > 3)}
            adj_matrix = adj_matrix.reindex(block_names)
            region_clients[region_clients[CLIENT_ID_COL].isin(block_names)][
                ['client_name', CLIENT_ID_COL, label_column]
            ].drop_duplicates(CLIENT_ID_COL).to_csv(f'data/{region.upper()}_network_figure_clusters.csv', index=False)

        else:

            block_names = pd.read_csv(f'data/{region.upper()}_network_figure_clusters_named.csv').set_index(
                CLIENT_ID_COL).coalition_name.to_dict()

        adj_matrix = adj_matrix.reindex(index = block_names)
        adj_matrices.append(adj_matrix)
        block_names_list.append(block_names)

    fig = figure_6_energy_positions(adj_matrices, block_names_list, ['CO', 'TX', 'IL', 'MA'])
    fig.savefig('figures/figure_6_energy_positions.pdf', bbox_inches='tight')
    fig.savefig('figures/figure_6_energy_positions.png', bbox_inches='tight', dpi=300)
