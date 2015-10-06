__author__ = 'Fabian Svara'

"""
Simplistic skeleton annotation format. This is deliberately kept flat,
we don't actually want to ever operate on these data, except when reading it
in and writing it out from / to some other format.

The classes below include attributes called "additional_data", which can be
used to store tool-specific additional information .
"""

class Node(object):
    def __init__(
            self, node_id, graph_id, coord, scaling, additional_meta=None):
        self.node_id = node_id
        self.graph_id = graph_id
        self.coord = coord
        self.coord_scaled = tuple([x*y for x, y in zip(coord, scaling)])
        self.additional_meta = additional_meta

    def __repr__(self):
        return 'Node at (%d, %d, %d)' % self.coord

    def __getattr__(self, item):
        return getattr(self.additional_meta, item)


class Edge(object):
    def __init__(self, graph_id, from_id, to_id, additional_meta=None):
        self.graph_id = graph_id
        self.from_id = from_id
        self.to_id = to_id
        self.additional_meta = additional_meta

    def __repr__(self):
        return 'Edge (%d, %d)' % (self.from_id, self.to_id)

    def __getattr__(self, item):
        return getattr(self.additional_meta, item)


class Graph(object):
    def __init__(self, graph_id, additional_meta=None):
        self.graph_id = graph_id
        self.additional_meta = additional_meta

    def __repr__(self):
        return 'Graph %d' % (self.graph_id, )

    def __getattr__(self, item):
        return getattr(self.additional_meta, item)


class Header(object):
    def __init__(self, source, scaling, additional_meta=None):
        self.source = source
        self.experiment_name = None
        self.scale = scaling
        self.additional_meta = additional_meta

    def __repr__(self):
        return 'Annotation for %s from %s' % (
            self.experiment_name, self.source, )

    def __getattr__(self, item):
        return getattr(self.additional_meta, item)