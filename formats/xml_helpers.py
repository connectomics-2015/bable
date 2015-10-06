__author__ = 'Fabian Svara'


def parse_attributes(xml_elem, attr_type_map):
    if xml_elem is None:
        return [None] * len(attr_type_map)

    attributes = xml_elem.attrib

    out = list()
    for cur_attr, cur_constructor in attr_type_map:
        try:
            out.append(cur_constructor(attributes[cur_attr]))
        except KeyError:
            out.append(None)

    return out


def cet_get_children(root, child_names):
    children = dict()
    for child in root:
        children[child.tag] = child

    as_requested = list()
    for cur_tag in child_names:
        try:
            as_requested.append(children[cur_tag])
        except KeyError:
            as_requested.append(None)

    return as_requested


def make_element(doc, tag_name, attr_type_map, attr_vals):
    elem = doc.createElement(tag_name)
    attr_vals_flat = []
    # Ensure that we can unpack lists / tuples into several attributes of one
    # XML tag.
    for cur_attr_val in attr_vals:
        if isinstance(cur_attr_val, (list, tuple)):
            attr_vals_flat.extend(cur_attr_val)
        else:
            attr_vals_flat.append(cur_attr_val)
    for (attr_name, _), attr_val in zip(attr_type_map, attr_vals_flat):
        if attr_val is None:
            continue
        elem.setAttribute(attr_name, unicode(attr_val))
    return elem