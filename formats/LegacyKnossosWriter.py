__author__ = 'Fabian Svara'

from legacyknossosskeleton.LegacySkeleton import LegacySkeletonAnnotation
from legacyknossosskeleton.LegacySkeleton import LegacySkeletonNode
from legacyknossosskeleton.LegacySkeleton import LegacySkeleton


class Writer(object):
    def __init__(self):
        pass

    def write(self, bable_anno, target, scaling=None):
        """
        Export the skeleton annotation to an instance of LegacySkeleton.

        @param scaling: 3-tuple
        @return: LegacySkeleton
        """

        if scaling is None:
            raise Exception('Must specify scaling to output legacy knossos '
                            'instance.')

        graph_id_to_legacyannotation = dict()
        for cur_g in bable_anno._graphs:
            a = LegacySkeletonAnnotation()

            try:
                a.color = cur_g.additional_meta.color
                a.comment = cur_g.additional_meta.comment
            except AttributeError:
                pass
            a.scaling = scaling
            graph_id_to_legacyannotation[cur_g.graph_id] = a

        unique_id_to_legacynode = dict()
        for cur_n in bable_anno._nodes:
            n = LegacySkeletonNode()
            a = graph_id_to_legacyannotation[cur_n.graph_id]
            am = cur_n.additional_meta
            x, y, z = cur_n.coord
            try:
                in_vp = am.in_vp
                in_mag = am.in_mag
                time = am.time
                radius = am.radius
                comment = am.comment
                n.from_scratch(a, x, y, z, inVp=in_vp, inMag=in_mag,
                               time=time, radius=radius)
                n.setComment(comment)
            except AttributeError:
                n.from_scratch(a, x, y, z)

            a.addNode(n)

            unique_id_to_legacynode[cur_n.node_id] = n

        for cur_e in bable_anno._edges:
            a = graph_id_to_legacyannotation[cur_e.graph_id]
            a.addEdge(
                unique_id_to_legacynode[cur_e.from_id],
                unique_id_to_legacynode[cur_e.to_id])

        s = LegacySkeleton()
        s.scaling = scaling
        for a in graph_id_to_legacyannotation.itervalues():
            s.add_annotation(a)

        return s
