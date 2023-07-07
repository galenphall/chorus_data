# This is run from the outer directory, not the replication_code directory, so we need to add the replication_code directory to the path.
import sys

sys.path.append('replication_code')

import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import normalized_mutual_info_score
from sklearn.naive_bayes import MultinomialNB
import load
from figures import figure_5_nmi_a, figure_1_records_per_year, figure_2_histogram, figure_5_nmi_b, \
    figure_4_blockmodel_projection, figure_6_energy_positions, figure_3_blockmodel
from hbsbm import get_bipartite_adjacency_matrix


def main():
    # if we're inside the replication_code folder, move up one level
    if os.getcwd().split('/')[-1] == 'replication_code':
        os.chdir('..')

    if not os.path.exists('figures'):
        os.mkdir('figures')

    if not os.path.exists('tables'):
        os.mkdir('tables')

    if not os.path.exists('data'):
        os.mkdir('data')

    """Load all position, bill, client data"""
    positions, clients, bills = load.positions(), load.clients(), load.bills()
    blockstates = load.blockstates()

    """Load Wisconsin data"""
    wi_blockstate = blockstates[('WI', 'lobbying')]
    wi_positions = positions[positions.state == 'WI']

    wi_graph = wi_blockstate.g
    wi_block_levels = pd.DataFrame({
        l: dict(zip(wi_graph.vp.name, wi_blockstate.project_partition(l, 0)))
        for l in range(len(wi_blockstate.levels))
    }).applymap(lambda l: f"wi{l}")

    wi_clients = clients[clients.state == 'WI'].copy()
    wi_bills = bills[bills.state == 'WI'].copy()

    for level in range(0, len(wi_blockstate.levels)):
        wi_bills[f'block_level_{level}'] = wi_bills.unified_bill_id.map(wi_block_levels[level])
        wi_clients[f'block_level_{level}'] = wi_clients.client_uuid.map(wi_block_levels[level])

    n_blocked_clients = wi_clients.drop_duplicates('client_uuid').block_level_0.notna().sum()
    n_blocked_bills = wi_bills.drop_duplicates('unified_bill_id').block_level_0.notna().sum()

    print(f"Interest groups (N={n_blocked_clients}) and bills (N={n_blocked_bills})")

    position_counts = pd.Series([*wi_graph.ep.weight]).value_counts()

    print(f"{position_counts[1]} support positions and {position_counts[-1]} oppose positions")

    ### Tables ###

    """Table 1: Summary statistics"""
    n_positions = positions.groupby(['state', 'record_type']).position_numeric.value_counts().unstack()
    percent_neutral = (n_positions.apply(lambda p: p[0] / sum(p), 1) * 100).round(1)
    avg_per_bill = positions.groupby(['state', 'record_type']).apply(
        lambda p: len(p) / p.unified_bill_id.nunique()).round(1)
    years_covered = positions.groupby(['state', 'record_type']).year.apply(lambda y: f"{min(y)}-{max(y)}")

    chamber_map = {
        'S': 'Senate',
        'H': 'House',
        'A': 'Assembly',
        'L': 'Unicameral'
    }

    positions['chamber'] = positions.unified_prefix.str[0].map(chamber_map)
    chambers_covered = positions.groupby(['state', 'record_type']).chamber.apply(
        lambda chambers: sorted({c for c in chambers.unique() if sum(chambers == c) > 100})).map(', '.join)

    table_1 = pd.concat([n_positions, percent_neutral, avg_per_bill, years_covered, chambers_covered], axis=1)
    table_1.columns = ['Support', 'Neutral', 'Oppose', '% Neutral', 'Average positions per bill', 'Years covered',
                       'Chambers covered']
    table_1.index.names = ['State', 'Record Type']
    table_1.to_excel('tables/summary_statistics.xlsx')

    """Table 2: Example block"""
    level_0_block_sizes = wi_clients.drop_duplicates('client_uuid').block_level_0.value_counts()
    highlighted_client_block = level_0_block_sizes.index[0]
    largest_block = wi_clients[wi_clients.block_level_0 == highlighted_client_block]
    table_2 = largest_block.drop_duplicates('client_uuid')
    table_2['ftm_final'] = table_2.apply(lambda r: r.ftm_final + ['', '*'][int(len(r.ftm_industry_merged) == 0)], 1)
    table_2 = table_2[['client_name', 'ftm_final']]
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

    client_block_level_0 = wi_clients.set_index('client_uuid').block_level_0.to_dict()
    bill_block_level_0 = wi_bills.set_index('unified_bill_id').block_level_0.to_dict()
    wi_matrix = wi_positions.pivot_table('position_numeric', 'client_uuid', 'unified_bill_id',
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
    bill_entropy_table = wi_bills[wi_bills.legiscan_bill.notna()].set_index('unified_bill_id')[['title']].join(
        bill_entropy).dropna()
    bill_entropy_table = bill_entropy_table.sort_values('bill_entropy').drop_duplicates('title')
    pd.concat([bill_entropy_table[::-1][:5], bill_entropy_table[:5]]).to_excel('tables/bill_entropy.xlsx')

    client_bill_cts = wi_matrix.T.groupby(bill_block_level_0).sum()
    client_bill_cts = client_bill_cts.loc[:, client_bill_cts.sum(0) > 0]
    client_entropy = client_bill_cts.apply(entropy).sort_values()[::-1]
    client_entropy.name = 'client_entropy'
    client_entropy_table = wi_clients.drop_duplicates('client_uuid').set_index('client_uuid')[['client_name']].join(
        client_entropy).dropna()
    client_entropy_table = client_entropy_table.sort_values('client_entropy')
    pd.concat([client_entropy_table[::-1][:5], client_entropy_table[:5]]).to_excel('tables/client_entropy.xlsx')

    ################
    ### Figures ###
    ################

    """Figure 1: Histogram of records per year"""
    records_per_year = positions[
        positions.client_uuid.notna() &
        (positions.year < 2022)].groupby(['record_type', 'year']).position_numeric.count().unstack().T

    fig = figure_1_records_per_year(records_per_year)
    fig.savefig('figures/figure_1_histogram.png', bbox_inches='tight', dpi=300)
    fig.savefig('figures/figure_1_histogram.pdf', bbox_inches='tight')

    """Figure 2: Histogram of records per bill and per client"""
    records_per_bill = positions[['state_unified_bill_id', 'record_type']].value_counts().unstack()
    records_per_bill_hist = records_per_bill.apply(lambda c: 2 ** (np.round(np.log2(c)))).apply(
        lambda c: c.value_counts())
    records_per_client = positions[['state_client_uuid', 'record_type']].value_counts().unstack()
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
        wi_clients.ftm_industry_merged.apply(lambda x: len(x) > 0) &
        wi_clients.block_level_0.notna()
        ].drop_duplicates('client_uuid')

    # Get all clients with guessed industry labels and block memberships
    guessed_sample = wi_clients[
        wi_clients.ftm_final.apply(lambda x: len(x) > 0) &
        wi_clients.block_level_0.notna() &
        wi_clients.ftm_industry_merged.apply(lambda x: len(x) == 0)
        ].drop_duplicates('client_uuid')

    # Compute NMI for each level of the hierarchy between the block memberships and the known and guessed industry labels
    known_nmi = {}
    guessed_nmi = {}
    for l in range(len(wi_blockstate.levels)):
        known_nmi[l] = normalized_mutual_info_score(
            known_ftm_sample.ftm_industry_merged.apply(lambda x: x[0] if len(x) > 0 else None),
            known_ftm_sample[f'block_level_{l}'])
        guessed_nmi[l] = normalized_mutual_info_score(guessed_sample.ftm_final,
                                                      guessed_sample[f'block_level_{l}'])

    fig, ax = figure_5_nmi_a(known_nmi, known_ftm_sample, guessed_nmi, guessed_sample)
    fig.savefig('figures/figure_5a_industry_nmi.pdf', bbox_inches='tight')
    fig.savefig('figures/figure_5a_industry_nmi.png', bbox_inches='tight', dpi=300)

    """Figure 5b: NMI for known and guessed issue labels in the Wisconsin blockmodel for each level of the hierarchy"""
    # Get all bills with metatopics and block memberships
    wi_bills_sample = wi_bills[
        wi_bills.ncsl_metatopics.apply(lambda x: (x is not None) and (len(x) > 0)) &
        wi_bills.block_level_0.notna()
        ].drop_duplicates('unified_bill_id')

    # Get all bills with topics and block memberships
    wi_bills_with_topics = wi_bills[
        wi_bills.ncsl_topics.apply(lambda x: (x is not None) and (len(x) > 0)) &
        wi_bills.block_level_0.notna()
        ].drop_duplicates('unified_bill_id')

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

    """Figure 6: client-level projection of blockstates for lobbying/testimony on energy and climate bills in four states"""

    adj_matrices = []
    block_names = []

    for region, record_type, level in [
        ('CO', 'lobbying', 0),
        ('TX', 'testimony', 0),
        ('IL', 'testimony', 1),
        ('MA', 'lobbying', 0)]:

        label_column = f'block_level_{level}'
        region_blockstate = blockstates[region, record_type]
        region_positions = positions[positions.state == region.upper()].copy()
        region_clients = clients[clients.state == region.upper()].copy()
        region_bills = bills[bills.state == region.upper()].copy()
        region_graph = region_blockstate.g
        region_block_levels = pd.DataFrame({
            l: dict(zip(region_graph.vp.name, region_blockstate.project_partition(l, 0)))
            for l in range(len(region_blockstate.levels))
        }).applymap(lambda l: f"{region}{l}")

        for l in range(0, len(region_blockstate.levels)):
            region_bills[f'block_level_{l}'] = region_bills.unified_bill_id.map(region_block_levels[l])
            region_clients[f'block_level_{l}'] = region_clients.client_uuid.map(region_block_levels[l])

        graph_positions = region_positions[
            region_positions.client_uuid.map(region_block_levels[2]).notna() &
            region_positions.ncsl_metatopics.astype(str).str.contains('energy')
            ]

        adj_matrix = get_bipartite_adjacency_matrix(graph_positions, (5, 3))
        block_names = region_clients.set_index('client_uuid')[label_column].astype(str).to_dict()

        if not os.path.exists(f'tables/{region.upper()}_network_figure_clusters_named.xlsx'):

            n_clients = abs(adj_matrix).groupby(block_names).apply(len)
            block_names = {k: v for k, v in block_names.items() if
                           (k in adj_matrix.index) and (v in n_clients) and (n_clients[v] > 3)}
            adj_matrix = adj_matrix.reindex(block_names)
            region_clients[region_clients.client_uuid.isin(block_names)][
                ['client_name', 'client_uuid', label_column]
            ].drop_duplicates('client_uuid').to_excel(f'tables/{region.upper()}_network_figure_clusters.xlsx')

        else:

            block_names = pd.read_excel(f'tables/{region.upper()}_network_figure_clusters_named.xlsx').set_index(
                'client_uuid').coalition_name.to_dict()

        adj_matrices.append(adj_matrix)
        block_names.append(block_names)

    fig = figure_6_energy_positions(adj_matrices, block_names, ['CO', 'TX', 'IL', 'MA'])
    fig.savefig('figures/figure_6_energy_positions.pdf', bbox_inches='tight')
    fig.savefig('figures/figure_6_energy_positions.png', bbox_inches='tight', dpi=300)
