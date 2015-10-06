from bable.formats.xml_helpers import make_element

__author__ = 'svara'

from xml.dom import minidom
from KnossosFormat import header_tags
from KnossosFormat import additional_header_tags
from KnossosFormat import Skeletons as XMLSkeletons


class Writer(object):
    def __init__(self):
        pass

    def write(self, bable_anno, target):
        """
        Export to on-disk .k.zip format.

        @param out_fname: str
        """

        doc = minidom.Document()

        things_e = doc.createElement('things')
        doc.appendChild(things_e)

        parameters_e = doc.createElement('parameters')
        for tag_name, attr_type_map, attr_names in header_tags:
            attr_vals = [getattr(bable_anno.header, x) for x in attr_names]
            cur_e = make_element(doc, tag_name, attr_type_map, attr_vals)
            parameters_e.appendChild(cur_e)
        for tag_name, attr_type_map, attr_names in additional_header_tags:
            try:
                attr_vals = [getattr(bable_anno.header.additional_meta, x)
                             for x in attr_names]
            except AttributeError:
                continue
            cur_e = make_element(doc, tag_name, attr_type_map, attr_vals)
            parameters_e.appendChild(cur_e)
        things_e.appendChild(parameters_e)

        comments_e = doc.createElement('comments')
        things_e.appendChild(comments_e)

        branchpoints_e = doc.createElement('branchpoints')
        things_e.appendChild(branchpoints_e)

        graph_uid_to_elem = dict()
        for g_id, am in bable_anno._iter_graphs():
            try:
                color = am.color
                comment = am.comment
            except AttributeError:
                color = (-1., -1., -1.,)
                comment = ''

            thing_e = make_element(
                doc, 'thing', XMLSkeletons.thing_tag_attrs,
                (g_id, color[0], color[1], color[2], comment))
            nodes_e = doc.createElement('nodes')
            edges_e = doc.createElement('edges')
            thing_e.appendChild(nodes_e)
            thing_e.appendChild(edges_e)
            graph_uid_to_elem[g_id] = (nodes_e, edges_e)
            things_e.appendChild(thing_e)

        for g_id, n_id, (x, y, z), _, am in bable_anno._iter_nodes():
            try:
                radius = am.radius
                in_vp = am.in_vp
                in_mag = am.in_mag
                time = am.time
            except AttributeError:
                radius = 1.5
                in_vp = 0
                in_mag = 1
                time = 0
            node_e = make_element(
                doc, 'node', XMLSkeletons.node_tag_attrs,
                (n_id, radius, x, y, z, in_vp, in_mag, time))
            nodes_e, _ = graph_uid_to_elem[g_id]
            nodes_e.appendChild(node_e)

            try:
                comment = am.comment
            except AttributeError:
                comment = None

            if comment is not None:
                comment_e = make_element(
                    doc, 'comment', XMLSkeletons.comment_tag_attrs,
                    (n_id, comment))
                comments_e.appendChild(comment_e)

            try:
                is_branchpoint = am.is_branchpoint
            except AttributeError:
                is_branchpoint = None

            if is_branchpoint:
                branchpoint_e = make_element(
                    doc, 'branchpoint', XMLSkeletons.branchpoint_tag_attrs,
                    (n_id, ))
                branchpoints_e.appendChild(branchpoint_e)

        for g_id, from_n_id, to_n_id, _ in bable_anno._iter_edges():
            edge_e = make_element(
                doc, 'edge', XMLSkeletons.edge_tag_attrs,
                (from_n_id, to_n_id))
            _, edges_e = graph_uid_to_elem[g_id]
            edges_e.appendChild(edge_e)

        with open(target, 'w') as fp:
            fp.write(doc.toprettyxml())