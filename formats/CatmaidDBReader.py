__author__ = 'Fabian Svara'

from ..BableInternalFormat import Node
from ..BableInternalFormat import Graph
from ..BableInternalFormat import Edge
from ..helpers import InvalidFormatException
from cat.connection import Connection


class NodeMeta(object):
    def __init__(self, user_id, radius, confidence):
        self.user_id = user_id
        self.radius = radius
        self.confidence = confidence


class Reader(object):
    def __init__(self):
        self.active_connection = None

    def read(self, bable_anno, source, project_id=None,
             skeleton_id=None, user=None, password=None, scaling=(1., 1., 1.)):
        self.active_connection = Connection(
            source, user, password, project_id)
        self.active_connection.login()

        skeleton = self.active_connection.fetch(
            '%d/1/1/compact-skeleton' % (skeleton_id, ))

        g_uid = bable_anno._graph_unique_id.get_id()
        g = Graph(g_uid)
        bable_anno._graphs.append(g)

        node_id_to_unique_id = dict()
        for n_1, n_2, user_id, x, y, z, radius, confidence in skeleton[0]:
            if n_1 in node_id_to_unique_id:
                continue

            cur_node_id = bable_anno._node_unique_id.get_id()
            node_id_to_unique_id[n_1] = cur_node_id

            cur_n = Node(cur_node_id, g_uid, [x, y, z], scaling)
            am = NodeMeta(user_id, radius, confidence)
            cur_n.additional_meta = am
            bable_anno._nodes.append(cur_n)

        for n_1, n_2, _, _, _, _, _, _ in skeleton[0]:
            if n_1 and n_2:
                n_1_uid = node_id_to_unique_id[n_1]
                n_2_uid = node_id_to_unique_id[n_2]
                cur_e = Edge(g_uid, n_2_uid, n_1_uid)
                bable_anno._edges.append(cur_e)