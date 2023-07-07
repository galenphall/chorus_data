import textwrap

import matplotlib as mpl
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def plot_bipartite(blockstate, filename=None, nedges=1000, hide_h=0, h_v_size=5.0, h_e_size=1.0, **kwargs):
    """
    Plot the graph and group structure.
    :param blockstate: gt.BlockState object
    :param filename: str; where to save the plot. if None, will not be saved
    :param nedges: int; subsample  to plot (faster, less memory)
    :param hide_h: int; wether or not to hide the hierarchy
    :param h_v_size: float; size of hierarchical vertices
    :param h_e_size: float; size of hierarchical edges
    :param **kwargs: keyword arguments passed to self.blockstate.draw method (https://graph-tool.skewed.de/static/doc/draw.html#graph_tool.draw.draw_hierarchy)
    """
    g = blockstate.g
    red = mpl.colors.to_rgba("crimson")
    yellowgreen = mpl.colors.to_rgba("yellowgreen")

    cm = mpl.colors.LinearSegmentedColormap.from_list("mycmap", [red, (1, 1, 1, 1), yellowgreen])

    blockstate.draw(layout='bipartite', output=filename,
                    subsample_edges=nedges, hshortcuts=1, hide=hide_h,
                    hvprops={'size': h_v_size},
                    heprops={'pen_width': h_e_size},
                    edge_pen_width=0.5,
                    edge_color=g.ep.weight.copy("double"),
                    eorder=g.ep.weight,
                    ecmap=(cm, 0.6), edge_gradient=[],
                    **kwargs,
                    )


def data_units_from_linewidth(linewidth, axis, reference='y', reverse=False):
    """
    Convert a linewidth in data units to linewidth in points.
    :param linewidth: width in data units (unless reverse is True)
    :param axis: plt.Axes object
    :param reference: 'x' or 'y' axis
    :param reverse: if True, convert from data units to inches
    :return:
    """
    fig: plt.Figure = axis.get_figure()
    if reference == 'x':
        # get bounding box of axes in inches
        length: float = fig.bbox_inches.width * axis.get_position().width  # axis length in inches
        value_range: np.array = np.diff(axis.get_xlim())  # data range
    elif reference == 'y':
        # get bounding box of axes in inches
        length: float = fig.bbox_inches.height * axis.get_position().height  # axis length in inches
        value_range: np.array = np.diff(axis.get_ylim())  # data range
    else:
        raise ValueError("reference must be either 'x' or 'y'")

    # Convert length scale to points
    points = length * fig.dpi

    # Scale linewidth to value range
    if reverse:
        return linewidth * points / value_range
    return linewidth / points * value_range


def plot_straight_edge_offset(lw, p1, p2, ax, color, direction):
    """
    Plot a straight edge between two points, with an offset.
    :param lw:
    :param p1:
    :param p2:
    :param ax:
    :param color:
    :param direction:
    :return:
    """
    # calculate vertical and horizontal width of line
    lw_dataunits = data_units_from_linewidth(lw, ax)
    lv = (p1 - p2) / np.linalg.norm(p1 - p2)
    lo = np.cross(lv, [0, 0, 1])[:2] * lw_dataunits
    theta = np.arctan(lo[0] / lo[1])
    dy, dx = lw_dataunits / [np.cos(theta), np.sin(theta)]

    # x1, y1 gives the line directly between nodes
    x1 = np.linspace(p1[0], p2[0])
    y1 = np.linspace(p1[1], p2[1])

    # fill between the connecting line and the offset, using whichever offset is smaller
    if abs(dy) > abs(dx):
        ax.fill_betweenx(y1, x1, x1 + direction * dx, color=color, interpolate=False)
    elif abs(dy) < abs(ax.get_ylim()[0] - ax.get_ylim()[1]):
        ax.fill_between(x1, y1, y1 + direction * dy, color=color, interpolate=False)
    else:
        print("Error on edge %s\ndx=%.2f, dy=%.2f" % (str(e), dx, dy))


def plot_curved_edge(lw, p1, p2, s1, s2, ax, color, direction, arrowstyle='-'):
    """
    Plot a curved edge between two points.
    :param lw: linewidth
    :param p1: start point
    :param p2: end point
    :param s1: width of start node
    :param s2: width of end node
    :param ax: axis
    :param color: color
    :param direction: direction of arrow
    :param arrowstyle: style of arrow
    :return: ax
    """
    if direction < 1:
        p1, p2, s1, s2 = p2, p1, s2, s1
    ax.annotate("", xy=p1, xycoords='data', xytext=p2, textcoords='data',
                arrowprops=dict(
                    arrowstyle=arrowstyle,
                    shrinkA=s2 ** 0.5 * 0.5, shrinkB=s1 ** 0.5 * 0.5,
                    patchA=None, patchB=None,
                    linewidth=lw,
                    color=color,
                    connectionstyle="arc3, rad=0.1", capstyle='butt'))

    return ax


def scatter_pie(x0, y0, ax, size, ratios, colors=None, **kwargs):
    """
    Scatter plot with pie chart markers.
    From https://stackoverflow.com/questions/56337732
    :param x0:
    :param y0:
    :param ax:
    :param size:
    :param ratios:
    :param colors:
    :param kwargs:
    :return:
    """
    if colors is None:
        colors = ['powderblue', 'yellowgreen', 'orangered']

    try:
        assert round(sum(ratios), 1) == 1
    except:
        pass

    xy = []
    s = []

    ratios = [0, *ratios]
    for i in range(len(ratios)):
        theta_0 = 2 * np.pi * sum(ratios[:i + 1])
        theta_1 = 2 * np.pi * sum(ratios[:i + 2])
        theta_range = np.linspace(theta_0, theta_1, 20)
        x, y = [0, *np.cos(theta_range)], [0, *np.sin(theta_range)]
        xy += [np.column_stack([x, y])]
        s += [np.abs(np.column_stack([x, y])).max()]

    for marker, scale, color in zip(xy, s, colors):
        ax.scatter(x0, y0, marker=marker,
                   s=scale ** 2 * size, facecolor=color,
                   edgecolor='k', **kwargs)


def cluster_agreement_plot(
        B,  # DataFrame: bipartite adjacency matrix
        c_dict,  # dict: cluster assignments
        ax=None,
        relation='agree',
        highlight=None,
        edgescale=20,
):
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    if highlight is None:
        highlight = [*c_dict.values()]

    assert isinstance(c_dict, dict)
    communities = {v: [k for k in c_dict if c_dict[k] == v] for v in set(c_dict.values())}

    pos_graph = PositionGraph()
    pos_graph.add_positions_from_dataframe(B)

    """Define agreement and disagreement graphs"""

    def cluster(G, c):
        C = nx.Graph()
        for n in G:
            C.add_node(n)

        for (u, v, d) in G.edges(data=True):

            w = d['weight']

            if (c[u], c[v]) not in C.edges:
                C.add_edge(c[u], c[v], weight=0, weights=[])

            if (c[v], c[u]) not in C.edges:
                C.add_edge(c[v], c[u], weight=0, weights=[])

            C.edges[c[u], c[v]]['weights'] += [w]
            C.edges[c[v], c[u]]['weights'] += [w]

        for e in C.edges:
            C.edges[e]['weight'] = sum(C.edges[e]['weights'])

        return C

    graphs = {
        p: cluster(pos_graph.agent_projection(p, 'sum'), c_dict)
        for p in [1, -1]
    }

    # Combine them using a directed graph
    C = nx.DiGraph()
    C.add_nodes_from(communities)
    for c1 in communities:
        for c2 in communities:
            if c1 < c2:
                if (c1, c2) in graphs[1].edges:
                    C.add_edge(c1, c2, weight=graphs[1][c1][c2]['weight'])
            elif c1 > c2:
                if (c1, c2) in graphs[-1].edges:
                    C.add_edge(c1, c2, weight=graphs[-1][c1][c2]['weight'])

    C = C.subgraph(highlight)

    """Calculate positions"""
    centers = nx.circular_layout(C)

    idxs = dict(zip(range(len(C)), C))
    order = sorted(idxs.values(), key=lambda x: int(
        x) if x.isdigit() else x)  # [idxs[v] for v in idxs if v % 2 == 0] + [idxs[v] for v in idxs if v % 2 == 1]

    centers = {order[i]: centers[idxs[i]] for i in idxs}

    scale = np.pi / (3 * len(communities))

    G_neg = pos_graph.agent_projection(-1, 'cossim')
    G_pos = pos_graph.agent_projection(1, 'cossim')
    G = type(G_neg)()
    G.add_nodes_from(c_dict.keys())

    E_neg = {(e[0], e[1]): e[2]['weight'] for e in G_neg.edges(data=True)}
    E_pos = {(e[0], e[1]): e[2]['weight'] for e in G_pos.edges(data=True)}

    for e in E_neg.keys() & E_pos.keys():
        w = E_pos[e] + E_neg[e]
        if w > 0:
            G.add_edge(*e, weight=w)

    G = G.subgraph([n for c in highlight for n in communities[c]])

    pos_f = {}

    for c in highlight:
        g = G.subgraph(communities[c])
        nodepos = nx.spring_layout(g, iterations=20, seed=42)
        nodepos = nx.rescale_layout_dict(nodepos, scale * 0.75)
        pos_f.update({n: nodepos[n] + centers[c] for n in nodepos})

    """Draw the nodes"""
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    node_bg = nx.draw_networkx_nodes(G,
                                     pos=pos_f,
                                     ax=ax,
                                     node_color='white',
                                     node_size=50,
                                     ).set_edgecolor('none')

    coalitions_by_node = list(map(c_dict.get, G))
    coalitions_ranked = dict(zip(list({*coalitions_by_node}), range(len(coalitions_by_node))))
    node_coalition_ranked = list(map(coalitions_ranked.get, coalitions_by_node))

    nodes = nx.draw_networkx_nodes(G,
                                   pos=pos_f,
                                   ax=ax,
                                   node_color=list(node_coalition_ranked),
                                   node_size=50,
                                   cmap='tab20',
                                   vmin=1,
                                   vmax=len(communities)
                                   )
    nodes.set_edgecolor('k')

    for c in communities:
        G_c = G.subgraph(communities[c])
        edges = nx.draw_networkx_edges(
            G_c,
            pos=pos_f,
            ax=ax,
            edge_color=[(0, 0, 0, e[2]['weight']) for e in G_c.edges(data=True)])

        if not isinstance(edges, list):
            edges.set_zorder(103)

    """Draw agreement and disagreement lines"""
    node_size = (data_units_from_linewidth(scale ** 0.5, ax, reverse=True) * 1.05) ** 2

    if relation != 'none':

        max_w = max([abs(e[2]['weight']) for e in C.edges(data=True)])

        for u, v in C.edges:
            w = C[u][v]['weight']
            if (((relation == 'agree') and (w > 0)) or
                    ((relation == 'oppose') and (w < 0)) or
                    (relation == 'both')):
                lw = abs(w) * edgescale / max_w
                color = mpl.colors.to_rgba(["crimson", "yellowgreen"][int(w > 0)])
                color = (*color[:3], 0.75)
                p1 = centers[u]
                p2 = centers[v]
                plot_curved_edge(lw, p1, p2, node_size * 0.95, node_size * 0.95, ax, color, direction=1)

    """Draw the cluster circles"""
    circles = nx.draw_networkx_nodes(C,
                                     pos=centers,
                                     ax=ax,
                                     node_color='white',
                                     node_size=node_size)
    circles.set_edgecolor('k')

    circles.set_zorder(100)
    nodes.set_zorder(105)

    """Label the coalitions"""
    for c in centers:
        n = len(communities[c])
        titletext = '\n'.join(textwrap.wrap(c, 20))
        ax.text(*(centers[c] * 1.6), f"{titletext}\nN = {n}",
                horizontalalignment='center',
                verticalalignment='center',
                fontdict={'size': 16})

    """Draw the pie charts"""
    ratios = {}
    for k in C:
        members = communities[k]
        if len(members) == 0:
            continue
        ratios[k] = B.reindex(members).stack().dropna().value_counts()
        for j in [0, -1, 1]:
            if j not in ratios[k].index:
                ratios[k].loc[j] = 0
        ratios[k] = ratios[k].loc[[0, 1, -1]]
        ratios[k] = (ratios[k].values / sum(ratios[k].values)).reshape(3, )

        scatter_pie(centers[k][0],
                    centers[k][1],
                    ax,
                    node_size * 1.2 ** 2,
                    ratios[k],
                    zorder=99,
                    )

    [ax.spines[s].set_visible(False) for s in ax.spines]

    return ax


class PositionGraph(nx.Graph):
    """
    bipartite_adj_matrix class for representing positions data as a bipartite graph with agents and bills as nodes.
    The main purpose of this class is to provide a convenient interface for constructing
    one-mode agent projections from positions data using different methods of aggregating.
    """

    def __init__(self):
        super().__init__()

    def add_agent(self, agent):
        assert isinstance(agent, str) or isinstance(agent, int)
        self.add_node(agent, bipartite=0)

    def add_bill(self, bill):
        assert isinstance(bill, str) or isinstance(bill, int)
        self.add_node(bill, bipartite=1)

    def add_positions_from_edgelist(self, elist):
        self.add_nodes_from(elist[:, 0], bipartite=0)
        self.add_nodes_from(elist[:, 1], bipartite=1)
        self.add_weighted_edges_from(elist)

    def add_positions_from_dataframe(self, dataframe):
        elist = dataframe.stack().reset_index(drop=False).values
        elist = elist[elist[:, 2] != 0]
        self.add_positions_from_edgelist(elist)

    def agent_projection(self, congruence, normalization='cossim', agents=None, bills=None):

        assert congruence in [1, -1, 'sum', 'pos_sum']

        assert normalization in ['sum', 'cossim', 'jaccard', 'directed_prop']

        if agents is None:
            agents = [n[0] for n in self.nodes(data=True) if n[1]['bipartite'] == 0]

        if bills is None:
            bills = [n[0] for n in self.nodes(data=True) if n[1]['bipartite'] == 1]

        if congruence in ('sum', 'pos_sum'):
            G_neg = self.agent_projection(-1, normalization, agents, bills)
            G_pos = self.agent_projection(1, normalization, agents, bills)
            G = type(G_neg)()

            E_neg = {(e[0], e[1]): e[2]['weight'] for e in G_neg.edges(data=True)}
            E_pos = {(e[0], e[1]): e[2]['weight'] for e in G_pos.edges(data=True)}

            for e in E_neg.keys() & E_pos.keys():
                w = E_neg[e] + E_pos[e]
                if (w > 0) or (congruence == 'sum'):
                    G.add_edge(*e, weight=w)

            return G

        else:

            def sum_weights(u, v):
                w = 0
                for nbr in set(self[u]) & set(self[v]):
                    if (self[u][nbr].get('weight', 1) * self[v][nbr].get('weight', 1) == congruence) & (nbr in bills):
                        w += congruence
                return w

            def cossim_weights(u, v):
                return sum_weights(u, v) / np.sqrt(self.degree(u) * self.degree(v))

            def jaccard_weights(u, v):
                return sum_weights(u, v) / len(set(self[u]) | set(self[v]))

            def directed_weights(u, v):
                return sum_weights(u, v) / self.degree(u)

            # Construct the agent-to-agent agreement graph
            if normalization == 'sum':
                G = nx.Graph()
                agfunc = sum_weights
            elif normalization == 'cossim':
                G = nx.Graph()
                agfunc = cossim_weights
            elif normalization == 'jaccard':
                G = nx.Graph()
                agfunc = jaccard_weights
            elif normalization == 'directed_prop':
                G = nx.DiGraph()
                agfunc = directed_weights
            else:
                raise ValueError(f"normalization '{normalization}' not implemented")

            agent_nodes = set(agents) & set(self.nodes)
            for u in agent_nodes:
                for v in agent_nodes:
                    if u != v:
                        G.add_edge(u, v, weight=agfunc(u, v))

            return G
