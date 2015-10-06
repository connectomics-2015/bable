__author__ = 'Fabian Svara'


from helpers import UniqueID
import formats


class BableAnnotation(object):
    """
    Class for importing / exporting skeletons from different formats. Format
    readers and writers are placed in formats/ and have to be registered in
    formats/__init__.py.

    The skeletons are stored in a simplistic internal format defined in
    BableInternalFormat.py.

    For importing and exporting, instances of the appropriate Writer and
    Reader classes (see formats/ for examples) are stored in BableAnnotation
    instances. This is to support reading and writing from sources that
    require or can benefit from state.

    See the examples in example.py.
    """

    def __init__(self):
        self.header = None
        self._edges = list()
        self._nodes = list()
        self._graphs = list()
        self._node_unique_id = UniqueID()
        self._graph_unique_id = UniqueID()
        self._node_unique_id_to_node = dict()
        self._writers = dict()
        self._readers = dict()

    def _iter_edges(self):
        for e in self._edges:
            yield e.graph_id, e.from_id, e.to_id, e.additional_meta

    def _iter_nodes(self):
        for n in self._nodes:
            yield n.graph_id, n.node_id, n.coord, n.coord_scaled, \
                  n.additional_meta

    def _iter_graphs(self):
        for g in self._graphs:
            yield g.graph_id, g.additional_meta

    def write(self, target_type, target, **kw):
        if not target_type in formats.writers:
            raise Exception('Unsupported output format. Use one of:\n%s' % (
                '\n'.join(formats.writers.keys())))
        if not target_type in self._writers:
            self._writers[target_type] = formats.writers[target_type]()
        W = self._writers[target_type]
        return W.write(self, target, **kw)

    def read(self, source_type, source, **kw):
        if not source_type in formats.readers:
            raise Exception('Unsupported input format. Use one of:\n%s' % (
                '\n'.join(formats.readers.keys())))
        if not source_type in self._readers:
            self._readers[source_type] = formats.readers[source_type]()
        R = self._readers[source_type]
        R.read(self, source, **kw)

    def info(self):
        print 'Supported readers: ' + str(formats.readers)
        print 'Supported writers: ' + str(formats.writers)

    def __repr__(self):
        return 'BableAnnotation with %d graphs, %d nodes, %d edges.' % (
            len(self._graphs), len(self._nodes), len(self._edges), )
