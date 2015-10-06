import copy


class InvalidFormatException(Exception):
    pass


class UniqueID(object):
    def __init__(self):
        self._cur_id = 0

    def get_id(self):
        self._cur_id += 1

        return self._cur_id


def copy_nodes(
        nodes, uid_map):
    """
    Generate Node instances for export. Takes a mapping dict from UIDs to
    Node instances, so that previously generated SkeletonNodes can be reused.

    :param nodes: list of Node
    :param uid_map: dict int -> SkeletonNode

    :return: list of tuple of Node, int
        Node and corresponding graph ID.
    """

    ret_nodes = []

    for n in nodes:
        if n.node_id in uid_map:
            ret_nodes.append(
                (uid_map[n.node_id], n.graph_id))
            continue

        node = copy.deepcopy(n)
        uid_map[n.node_id] = node
        ret_nodes.append((node, n.graph_id))

    return ret_nodes