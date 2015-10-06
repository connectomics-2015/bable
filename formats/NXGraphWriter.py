__author__ = 'Fabian Svara'

try:
    import networkx as nx
    nx_available = True
except ImportError:
    nx_available = False

from ..helpers import copy_nodes


class Writer(object):
    def __init__(self):
        pass

    def write(self, bable_anno, target, reuse_nodes=True, by_graph=True):
        """
        Convert the skeleton annotation to a NetworkX graph of Node
        instances.

        @param scaling: 3-tuple
        @param reuse_nodes: bool
            If True, re-use previously exported Node objects. Useful
            e.g. to create kd-trees and NetworkX graphs of the same
            Node instances.
        @param by_graph: bool
            If True, return a list of NetworkX graphs, one for each thing.
            Otherwise, all nodes will be part of the same graph.
        @return: NetworkX graph or list of NetworkX graphs
            If by_graph is True, return a list or graphs, otherwise, return a
            graph.
        """

        if not nx_available:
            raise ImportError('NetworkX is not available, '
                              'skeleton_to_nx_graph() can not be used.')

        if not reuse_nodes:
            bable_anno._node_unique_id_to_node = dict()

        graph_id_to_nx_graph = dict()

        G = None
        for cur_graph in bable_anno._graphs:
            # TODO
            # Export graph meta to networkx
            if by_graph:
                graph_id_to_nx_graph[cur_graph.graph_id] = nx.Graph()
            else:
                if G is None:
                    G = nx.Graph()
                graph_id_to_nx_graph[cur_graph.graph_id] = G

        for node, g_id in copy_nodes(
                bable_anno._nodes, bable_anno._node_unique_id_to_node):
            graph_id_to_nx_graph[g_id].add_node(node)

        for cur_e in bable_anno._edges:
            from_n = bable_anno._node_unique_id_to_node[cur_e.from_id]
            to_n = bable_anno._node_unique_id_to_node[cur_e.to_id]

            graph_id_to_nx_graph[cur_e.graph_id].add_edge(from_n, to_n)

        if by_graph:
            return graph_id_to_nx_graph.values()
        else:
            return G
