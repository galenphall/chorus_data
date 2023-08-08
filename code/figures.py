import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from ..code.utils import CLIENT_ID_COL, BILL_ID_COL, cluster_agreement_plot, plot_bipartite


def figure_1_records_per_year(records_per_year):
    """
    Plot the records per year line plots in figure 1
    :param records_per_year:
    :return:
    """
    fig, ax = plt.subplots(1, 1, figsize=(5, 3))
    records_per_year.plot(
        mec='k',
        marker='o',
        grid=True,
        ax=ax)
    current_values = plt.gca().get_yticks()
    ax.set_xticks(np.arange(1997, 2023, 2))
    ax.set_xticklabels(ax.get_xticks(), rotation=45, ha='right')
    ax.set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    ax.set_ylabel("Positions")
    ax.set_xlabel("Year")
    ax.legend(title='Record type')
    return fig


def figure_2_histogram(records_per_bill_hist: pd.Series, records_per_client_hist: pd.Series):
    """
    Plot the histograms in figure 2
    :param records_per_bill_hist: a pd.Series containing the histogram of records per bill
    :param records_per_client_hist: a pd.Series containing the histogram of records per client
    :return:
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3), gridspec_kw={'wspace': 0}, sharey=True, sharex=True)

    for record_type in records_per_bill_hist.columns:
        records_per_bill_hist[record_type].plot(marker='o', mec='k', linewidth=1, label=record_type, ax=ax1)
    ax1.set_yscale('log')
    ax1.set_xscale('log')
    ax1.set_ylabel("Number of bills/interest groups")
    ax1.set_xlabel("Records per bill")
    ax1.grid(zorder=-1)
    ax1.set_title('Bills')

    for record_type in records_per_client_hist.columns:
        records_per_client_hist[record_type].plot(marker='o', mec='k', linewidth=1, label=record_type, ax=ax2)
    ax2.set_yscale('log')
    ax2.set_xscale('log')
    ax2.set_xlabel("Records per interest group")
    ax2.set_title('Interest Groups')
    ax2.grid(zorder=-1)
    ax2.legend()
    return fig


def figure_3_blockmodel(wi_blockstate, filename="figure_3_blockmodel_spaghetti.png"):
    """
    Plot the blockmodel for Wisconsin using the "spaghetti" plot
    :param wi_blockstate:
    :param filename:
    :return:
    """
    # imported here because this requires graph-tool
    plot_bipartite(wi_blockstate, f"figures/{filename}", nedges=5000)


def figure_4_blockmodel_projection(wi_positions, wi_block_levels, wi_clients, block_level=3):
    """
    Plot the blockmodel projection for Wisconsin at a given block level
    :param wi_positions:
    :param wi_block_levels:
    :param wi_clients:
    :param label_column:
    :return:
    """
    label_column = f'block_level_{block_level}'

    graph_positions = wi_positions[
        wi_positions[CLIENT_ID_COL].map(wi_block_levels[0]).notna() &
        wi_positions[BILL_ID_COL].map(wi_block_levels[0]).notna()
        ]

    c = wi_clients.set_index(CLIENT_ID_COL)[label_column].astype(str).to_dict()
    B = np.sign(graph_positions.pivot_table('position_numeric', CLIENT_ID_COL, BILL_ID_COL, 'sum'))
    B = B.loc[B.index.map(c).notna()]
    B = B.loc[abs(B).sum(1) > 0]

    c = {k: v for k, v in c.items() if k in B.index}

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    cluster_agreement_plot(B, c, relation='both', ax=ax)
    return fig


def figure_5_nmi_a(known_nmi, known_ftm_sample, guessed_nmi, guessed_sample):
    """
    Plot the NMI between block-level assignments and FTM classification
    :param known_nmi:
    :param known_ftm_sample:
    :param guessed_nmi:
    :param guessed_sample:
    :return:
    """
    fig, ax = plt.subplots(1, 1, figsize=(5, 3))
    ax.set_title("NMI between block-level assignments and\nFTM classification")
    pd.Series(known_nmi)[range(4)].plot(
        marker='o',
        mfc='w',
        mec='cornflowerblue',
        color='cornflowerblue',
        label=f"FollowTheMoney (N={known_ftm_sample[CLIENT_ID_COL].nunique()})")
    pd.Series(guessed_nmi)[range(4)].plot(
        marker='o',
        mfc='w',
        mec='orange',
        color='orange',
        label=f"Naive Bayes (N={guessed_sample[CLIENT_ID_COL].nunique()})")
    ax.set_xlabel("Block hierarchy level")
    ax.set_ylabel("NMI")
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 1, 2, 3])
    ax.legend(title='Source of classification')
    return fig, ax


def figure_5_nmi_b(topic_nmi, wi_bills_with_topics, meta_topic_nmi, wi_bills_sample):
    """
    Plot the NMI between block-level assignments and NCSL topic category
    :param topic_nmi:
    :param wi_bills_with_topics:
    :param meta_topic_nmi:
    :param wi_bills_sample:
    :return:
    """
    fig, ax = plt.subplots(1, 1, figsize=(5, 3))
    ax.set_title("NMI between block-level assignments and\nNCSL topic category")
    pd.Series(topic_nmi)[range(4)].plot(
        marker='o',
        mfc='w',
        mec='cornflowerblue',
        color='cornflowerblue',
        label=f"Topic (N={wi_bills_with_topics[BILL_ID_COL].nunique()})")
    pd.Series(meta_topic_nmi)[range(4)].plot(
        marker='o',
        mfc='w',
        mec='orange',
        color='orange',
        label=f"Meta-Topic (N={wi_bills_sample[BILL_ID_COL].nunique()})")
    ax.set_xlabel("Block hierarchy level")
    ax.set_ylabel("NMI")
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 1, 2, 3])
    ax.legend(title='Source of classification')
    return fig


def figure_6_energy_positions(state_adj_matrices, state_block_names, states):
    """
    Plot the projection of client positions on energy bills for each state
    :param state_adj_matrices:
    :param state_block_names:
    :param states:
    :return:
    """
    fig, axes = plt.subplots(
        2, 2, figsize=(20, 20),
        gridspec_kw={'wspace': 0.1, 'hspace': 0.1},
    )

    for adj_matrix, block_names, state, ax in zip(
            state_adj_matrices, state_block_names, states, axes.flatten()
    ):
        cluster_agreement_plot(adj_matrix, block_names, relation='both', ax=ax)
        ax.set_title(state, fontsize=20, fontweight='bold')
        ax.spines['top'].set_visible(True)

    return fig
