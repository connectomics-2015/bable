__author__ = 'Fabian Svara'

"""
Format info for Knossos files (NML and .k.zip) used by KnossosReader and
KnossosWriter.
"""

def bool_str(from_str):
    """
    bool(str) will return False only from empty strings, but when reading XML we
    '0' to mean False.
    """
    return bool(int(from_str))

# Additional knossos-specific meta information not part of the core bable
# data representation.
#

class NodeMeta(object):
    def __init__(self, in_vp=None, in_mag=None, time=None, radius=None,
                 comment = None, is_branchpoint=False):
        self.in_vp = in_vp
        self.in_mag = in_mag
        self.time = time
        self.radius = radius
        self.comment = comment
        if not is_branchpoint:
            self.is_branchpoint = False
        else:
            self.is_branchpoint = True


class EdgeMeta(object):
    def __init__(self):
        pass


class GraphMeta(object):
    def __init__(self, color=None, comment=None):
        self.color = color
        self.comment = comment

class HeaderMeta(object):
    def __init__(self):
        # We do not currently support the activeNode header, because in this
        # design, the node IDs are undefined until a KnossosFile class is
        # converted into an on-disk Knossos file. We could find some
        # work-around, but this doesn't seem like a priority currently,
        # since you can just set editPosition if you want to direct a tracer
        # to some particular location.

        self.last_saved_in = None
        self.created_in = None
        self.dataset_path = None
        self.movement_area = (None, ) * 6
        self.comment_locking_enabled = None
        self.locking_radius = None
        self.lock_to_comment = None
        self.time = None
        self.time_checksum = None
        self.edit_position = (None, ) * 6
        self.skeleton_vp_state = (None, ) * 18
        self.vp_settings_zoom = (None, ) * 4


# Description of knossos file header XML
#

class Header(object):
    experiment_tag_attrs = [
        ('name', unicode),
    ]

    last_saved_tag_attrs = [
        ('version', unicode),
    ]

    created_tag_attrs = [
        ('version', unicode),
    ]

    dataset_tag_attrs = [
        ('path', unicode),
    ]

    active_node_tag_attrs = [
        (id, int),
    ]

    movement_area_tag_attrs = [
        ('min.x', int),
        ('min.y', int),
        ('min.z', int),
        ('max.x', int),
        ('max.y', int),
        ('max.z', int),
    ]

    scale_tag_attrs = [
        ('x', float),
        ('y', float),
        ('z', float),
    ]

    radius_locking_tag_attrs = [
        ('enableCommentLocking', bool_str),
        ('lockingRadius', int),
        ('lockToNodesWithComment', unicode),
    ]

    time_tag_attrs = [
        ('ms', int),
        ('checksum', unicode),
    ]

    edit_position_tag_attrs = [
        ('x', int),
        ('y', int),
        ('z', int),
    ]

    skeleton_vp_state_attrs = [
        ('E0', float),
        ('E1', float),
        ('E2', float),
        ('E3', float),
        ('E4', float),
        ('E5', float),
        ('E6', float),
        ('E7', float),
        ('E8', float),
        ('E9', float),
        ('E10', float),
        ('E11', float),
        ('E12', float),
        ('E13', float),
        ('E14', float),
        ('E15', float),
        ('translateX', float),
        ('translateY', float),
    ]

    vp_settings_zoom_attrs = [
        ('XYPlane', float),
        ('XZPlane', float),
        ('YZPlane', float),
        ('SkelVP', float),
    ]

# Description of Knossos file skeleton XML
#


class Skeletons(object):
    thing_tag_attrs = [
        ('id', int),
        ('color.r', float),
        ('color.g', float),
        ('color.b', float),
        ('color.a', float),
        ('comment', unicode),
    ]

    node_tag_attrs = [
        ('id', int),
        ('radius', float),
        ('x', int),
        ('y', int),
        ('z', int),
        ('inVp', int),
        ('inMag', int),
        ('time', int),
    ]

    edge_tag_attrs = [
        ('source', int),
        ('target', int),
    ]

    comment_tag_attrs = [
        ('node', int),
        ('content', unicode),
    ]

    branchpoint_tag_attrs = [
        ('id', int)
    ]
    
# Knossos NML file headers that map directly to Bable internal format
#

header_tags = [
    ('experiment',
    Header.experiment_tag_attrs,
    ('experiment_name', )),
    #
    ('scale',
    Header.scale_tag_attrs,
    ('scale', )),
    #
]

# Knossos NML file headers that will be stored as Bable internal format
# additional meta info
#
    
additional_header_tags = [
    ('lastsavedin',
    Header.last_saved_tag_attrs,
    ('last_saved_in', )),
    #
    ('createdin',
    Header.created_tag_attrs,
    ('created_in', )),
    #
    ('dataset',
    Header.dataset_tag_attrs,
    ('dataset_path', )),
    #
    ('MovementArea',
    Header.movement_area_tag_attrs,
    ('movement_area', )),
    #
    ('RadiusLocking',
    Header.radius_locking_tag_attrs,
    ('comment_locking_enabled',
     'locking_radius',
     'lock_to_comment', )),
    #
    ('time',
    Header.time_tag_attrs,
    ('time',
     'time_checksum', )),
    #
    ('editPosition',
    Header.edit_position_tag_attrs,
    ('edit_position', )),
    #
    ('skeletonVPState',
    Header.skeleton_vp_state_attrs,
    ('skeleton_vp_state', )),
    #
    ('vpSettingsZoom',
    Header.vp_settings_zoom_attrs,
    ('vp_settings_zoom', )),
]





