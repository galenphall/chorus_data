import networkx as nx
import numpy as np


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
        self.add_node(agent, bipartite = 0)

    def add_bill(self, bill):
        assert isinstance(bill, str) or isinstance(bill, int)
        self.add_node(bill, bipartite = 1)

    def add_positions_from_edgelist(self, elist):
        self.add_nodes_from(elist[:, 0], bipartite=0)
        self.add_nodes_from(elist[:, 1], bipartite=1)
        self.add_weighted_edges_from(elist)

    def add_positions_from_dataframe(self, dataframe):
        elist = dataframe.stack().reset_index(drop = False).values
        elist = elist[elist[:, 2] != 0]
        self.add_positions_from_edgelist(elist)

    def agent_projection(self, congruence, normalization='cossim', agents=None, bills=None):

        assert congruence in [1, -1, 'sum', 'pos_sum']

        assert normalization in ['sum', 'cossim', 'jaccard', 'directed_prop']

        if agents is None:
            agents = [n[0] for n in self.nodes(data = True) if n[1]['bipartite'] == 0]

        if bills is None:
            bills = [n[0] for n in self.nodes(data = True) if n[1]['bipartite'] == 1]

        if congruence in ('sum', 'pos_sum'):
            G_neg = self.agent_projection(-1, normalization, agents, bills)
            G_pos = self.agent_projection(1, normalization, agents, bills)
            G = type(G_neg)()

            E_neg = {(e[0], e[1]) : e[2]['weight'] for e in G_neg.edges(data = True)}
            E_pos = {(e[0], e[1]) : e[2]['weight'] for e in G_pos.edges(data = True)}

            for e in E_neg.keys() & E_pos.keys():
                w = E_neg[e] + E_pos[e]
                if (w > 0) or (congruence == 'sum'):
                    G.add_edge(*e, weight = w)

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
                        G.add_edge(u, v, weight = agfunc(u, v))

            return G