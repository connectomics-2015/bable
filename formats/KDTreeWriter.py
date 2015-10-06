__author__ = 'Fabian Svara'

try:
    from spatial import KDtree
    kd_available = True
except ImportError:
    kd_available = False
from ..helpers import copy_nodes


class Writer(object):
    def __init__(self):
        pass

    def write(self, bable_anno, target, reuse_nodes=True):
        """

        @param scaling: 3-tuple
        @param reuse_nodes: bool
            If True, re-use previously exported SkeletonNode objects. Useful
            e.g. to create kd-trees and NetworkX graphs of the same
            SkeletonNode instances.
        @return: KDtree
        """

        if not kd_available:
            raise ImportError('kd-tree form scipy is not available, '
                              'can not write kd trees.')

        if not reuse_nodes:
            bable_anno._node_unique_id_to_node = dict()

        nodes = copy_nodes(
                bable_anno._nodes, bable_anno._node_unique_id_to_node)

        kd_tree = KDtree([x for x, y in nodes])

        return kd_tree
