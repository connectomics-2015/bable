try:
    from scipy.spatial import cKDTree as kdt
    have_ctree = True
except ImportError:
    from scipy.spatial import KDTree as kdt
    have_ctree = False
import numpy as np

if not have_ctree:
    print('Could not import C kd-Tree implementation (cKDTree) from scipy. '
          'Using slow fallback. Consider updating scipy.')


class KDtree:
    """
    scipy based KD-tree wrapper class that allows efficient spatial searches
    for SkeletonNode instance or arbitrary python objects.
    """

    def __init__(self, nodes, coords=None):
        # spatial.cKDtree is reported to be 200-1000 times faster
        # however, query_ball_point is only included in very recent scipy
        # packages, not yet shipped
        # with Ubuntu 12.10 (and a manual scipy installation can be  messy)

        self.lookup = list(nodes)

        if not coords:
            self.coords = np.array([x.coord_scaled for x in nodes])

            self.tree = kdt(self.coords)
        else:
            self.coords = coords
            # the ordering of coords and nodes must be the same!!!
            self.tree = kdt(self.coords)

        return

    def __str__(self):
        return ', '.join([str(x) for x in self.lookup])

    # enables efficient pickling of cKDtree
    def __getstate__(self):
        return self.lookup, self.coords

    # enables efficient pickling of cKDtree
    def __setstate__(self, state):
        self.lookup, coords = state
        self.tree = kdt(self.coords)

    def query_k_nearest(self, coords, k=1, return_dists=False):
        # This function was written to replace queryNN which is still kept
        # for backwards compatibility
        dists, obj_lookup_IDs = self.tree.query(np.array(coords), k=k)
        try:
            if not return_dists:
                return [self.lookup[ID] for ID in obj_lookup_IDs.tolist()]
            else:
                return [self.lookup[ID] for ID in obj_lookup_IDs.tolist()],dists
        except AttributeError:
            if not return_dists:
                return self.lookup[obj_lookup_IDs]
            else:
                return self.lookup[obj_lookup_IDs], dists

    def query_nearest_node(self, coords):
        if isinstance(coords[0], (int, float)):
            coords = [coords]
        return self.queryNN(coords)

    def queryNN(self, coords):
        # element num 1 contains the array indices for our lookup table
        nodes = [self.lookup[i] for i in
            list(self.tree.query(np.array(coords)))[1].tolist()]

        return nodes

    def query_ball_point(self, coord, radius):
        listOfNodeLists = self.tree.query_ball_point(np.array(coord), radius)
        resultList = []
        for listOfNodes in listOfNodeLists:
            if type(listOfNodes) is list:
                resultList.append([self.lookup[i] for i in listOfNodes])
            else:
                resultList.append(self.lookup[listOfNodes])

        # this would make the list flat:
        # resultList = [item for sublist in resultList for item in sublist]

        return resultList

    def query_ball_tree(self, other, radius):
        results = self.tree.query_ball_tree(other.tree, radius)
        return results