__author__ = 'Fabian Svara'

import copy
from ..BableInternalFormat import *


class Reader(object):
    def __init__(self):
        pass

    def read(self, bable_anno, source, **kw):
        """
        Combine the skeleton annotation data contained in a BableAnnotation
        instance anno into bable_anno.

        @aparam bable_anno: BableAnnotation
        @param source: BableAnnotation
        @return: None
        """

        to_unique_node_id = dict()
        to_unique_graph_id = dict()

        for orig_g in source._graphs:
            graph_id = bable_anno._graph_unique_id.get_id()
            to_unique_graph_id[orig_g.graph_id] = graph_id

            cur_g = copy.deepcopy(orig_g)
            cur_g.graph_id = graph_id
            bable_anno._graphs.append(cur_g)

        for orig_n in source._nodes:
            graph_id = to_unique_graph_id[orig_n.graph_id]
            node_id = bable_anno._node_unique_id.get_id()
            to_unique_node_id[orig_n.node_id] = node_id

            cur_n = copy.deepcopy(orig_n)
            cur_n.node_id = node_id
            cur_n.graph_id = graph_id

            bable_anno._nodes.append(cur_n)

        for g_id, from_id, to_id, additional_meta in source._iter_edges():
            graph_id = to_unique_graph_id[g_id]

            from_id = to_unique_node_id[from_id]
            to_id = to_unique_node_id[to_id]
            cur_e = Edge(graph_id, from_id, to_id,
                         additional_meta=copy.deepcopy(additional_meta))
            bable_anno._edges.append(cur_e)

