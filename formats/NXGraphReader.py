__author__ = 'Fabian Svara'

import copy
from ..BableInternalFormat import *

class Reader(object):
    def __init__(self):
        pass

    def read(self, bable_anno, source, **kw):
        """
        Combine NetworkX Graph of Node instances into BableAnnotation. The
        entire graph being imported will  have the same graph id.

        @param bable_anno: BableAnnotion
        @param source: NetworkX graph
        @return: None
        """

        orig_node_to_unique_id = dict()

        graph_id = bable_anno._graph_unique_id.get_id()

        g = Graph(graph_id)
        bable_anno._graphs.append(g)

        print source
        for n_orig in source.nodes_iter():
            cur_id = bable_anno._node_unique_id.get_id()
            orig_node_to_unique_id[n_orig] = cur_id

            cur_n = copy.deepcopy(n_orig)
            cur_n.node_id = cur_id
            cur_n.graph_id = graph_id
            bable_anno._nodes.append(cur_n)

        for n_1, n_2 in source.edges_iter():
            n_1_id = orig_node_to_unique_id[n_1]
            n_2_id = orig_node_to_unique_id[n_2]
            cur_e = Edge(graph_id=graph_id, from_id=n_1_id, to_id=n_2_id)
            bable_anno._edges.append(cur_e)