from bable.formats.xml_helpers import parse_attributes

__author__ = 'Fabian Svara'

from zipfile import ZipFile
import xml.etree.cElementTree as cet
from ..helpers import InvalidFormatException
from KnossosFormat import header_tags
from KnossosFormat import additional_header_tags
from ..BableInternalFormat import *
from KnossosFormat import HeaderMeta as AdditionalHeader
from KnossosFormat import NodeMeta as AdditionalNode
from KnossosFormat import GraphMeta as AdditionalGraph
from KnossosFormat import Skeletons as XMLSkeletons


def is_kzip(fname):
    try:
        ZipFile(fname)
        return True
    except:
        return False


def is_nml(fname):
    if fname.lower().endswith('.nml'):
        return True
    else:
        return False


class Reader(object):
    def __init__(self):
        # Cache to avoid decompressing repeatedly
        self._annotation_file_cache = dict()

    def _get_knossos_file_annotation_xml(self, in_fname):
        if in_fname in self._annotation_file_cache:
            return self._annotation_file_cache[in_fname]

        if is_kzip(in_fname):
            zipper = ZipFile(in_fname)
            if not 'annotation.xml' in zipper.namelist():
                raise InvalidFormatException(
                    'Knossos .k.zip file %s does not contain annotation.xml' % (
                        in_fname, ))
            xml_string = zipper.read('annotation.xml')
        elif is_nml(in_fname):
            with open(in_fname, 'r') as fp:
                xml_string = fp.read()
        else:
            raise InvalidFormatException(
                'Invalid knossos file: %s' % (in_fname, ))

        self._annotation_file_cache[in_fname] = xml_string

        return xml_string

    def header_from_knossos_file(self, bable_anno, in_fname):
        bable_anno.header = Header(None, None, None)
        bable_anno.header.additional_meta = AdditionalHeader()

        xml_str = self._get_knossos_file_annotation_xml(in_fname)
        root = cet.fromstring(xml_str)
        parameters_e = root.find('parameters')

        for cur_tag_name, cur_tag_attrs, cur_targets in header_tags:
            cur_tag_e = parameters_e.find(cur_tag_name)
            ret = parse_attributes(cur_tag_e, cur_tag_attrs)
            if len(cur_targets) == 1 and len(ret) > 1:
                ret = [ret]
            for cur_target, cur_ret in zip(cur_targets, ret):
                setattr(bable_anno.header, cur_target, cur_ret)

        for cur_tag_name, cur_tag_attrs, cur_targets in additional_header_tags:
            cur_tag_e = parameters_e.find(cur_tag_name)
            ret = parse_attributes(cur_tag_e, cur_tag_attrs)
            if len(cur_targets) == 1 and len(ret) > 1:
                ret = [ret]
            for cur_target, cur_ret in zip(cur_targets, ret):
                setattr(bable_anno.header.additional_meta, cur_target, cur_ret)

        bable_anno.header.source = 'Knossos'

    def read(self, bable_anno, source, scaling=None):
        """
        Add skeleton annotations from a knossos file. Node and graph IDs are
        not preserved from the file.
        """

        if scaling is None:
            raise Exception('Must specifiy scaling to read knossos file.')

        self.header_from_knossos_file(bable_anno, source)

        xml_str = self._get_knossos_file_annotation_xml(source)
        root = cet.fromstring(xml_str)

        # This dictionary temporarily holds the mapping from node IDs local
        # to the current knossos file to unique IDs given out while loading.
        # We make no attempt to preserve node IDs.
        local_node_id_to_unique_id = dict()
        local_graph_id_to_unique_id = dict()
        local_node_id_to_node = dict()

        for cur_graph_e in root.findall('thing'):
            graph_id, r, g, b, a, comment = parse_attributes(
                cur_graph_e, XMLSkeletons.thing_tag_attrs)

            cur_graph_id = bable_anno._graph_unique_id.get_id()
            cur_graph = Graph(
                graph_id=cur_graph_id, additional_meta=None)
            cur_graph.additional_meta = AdditionalGraph(
                color=(r, g, b, a), comment=comment)
            bable_anno._graphs.append(cur_graph)
            local_graph_id_to_unique_id[graph_id] = cur_graph_id

            cur_nodes_e = cur_graph_e.find('nodes')
            for cur_node_e in cur_nodes_e.findall('node'):
                node_id, radius, x, y, z, in_vp, in_mag, timestamp = \
                    parse_attributes(cur_node_e, XMLSkeletons.node_tag_attrs)
                cur_node_id = bable_anno._node_unique_id.get_id()
                local_node_id_to_unique_id[node_id] = cur_node_id
                cur_node = Node(
                    node_id=cur_node_id,
                    graph_id=cur_graph_id,
                    coord=(x, y, z),
                    scaling=scaling)
                cur_node.additional_meta = AdditionalNode(
                    radius=radius,
                    in_vp=in_vp,
                    in_mag=in_mag,
                    time=timestamp, )
                bable_anno._nodes.append(cur_node)
                local_node_id_to_node[node_id] = cur_node

        # It is important to read edges after reading nodes, since otherwise
        # the edges could refer to nodes that have not yet been encountered,
        # since they can be between different things (graphs). This is a design
        # issue in the Knossos skeleton XML format (NML).
        for cur_graph_e in root.findall('thing'):
            graph_id, _, _, _, _, _ = parse_attributes(
                cur_graph_e, XMLSkeletons.thing_tag_attrs)
            cur_graph_id = local_graph_id_to_unique_id[graph_id]
            cur_edges_e = cur_graph_e.find('edges')
            for cur_edge_e in cur_edges_e.findall('edge'):
                source_node_id, target_node_id = parse_attributes(
                    cur_edge_e, XMLSkeletons.edge_tag_attrs)
                try:
                    cur_edge = Edge(
                        graph_id=cur_graph_id,
                        from_id=local_node_id_to_unique_id[source_node_id],
                        to_id=local_node_id_to_unique_id[target_node_id])
                except KeyError:
                    raise InvalidFormatException(
                        'File %s contains edge with non-existant node: (%d, '
                        '%d).' % (source, source_node_id, target_node_id, ))
                bable_anno._edges.append(cur_edge)

        for comment_e in root.iter('comment'):
            node_id, content = parse_attributes(
                comment_e, XMLSkeletons.comment_tag_attrs)
            try:
                n = local_node_id_to_node[node_id]
            except KeyError:
                print('Skipping comment on non-existing node %d' % (node_id, ))
                continue
            n.additional_meta.comment = content

        for branchpoint_e in root.iter('branchpoint'):
            node_id,  = parse_attributes(
                branchpoint_e, XMLSkeletons.branchpoint_tag_attrs)
            try:
                n = local_node_id_to_node[node_id]
            except KeyError:
                print('Skipping branchpoint flag on non-existing node %d' % (
                    node_id, ))
                continue
            n.is_branchpoint = True