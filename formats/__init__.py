__author__ = 'Fabian Svara'

"""
To implement new import / export functionality, put your code in (a) python
file(s). For import, implement a class called Reader with a method read(),
for export, implement a class called Writer with a method write(). Then,
add the name of the format and the package from which Reader or Writer can be
imported to the lists _load_output and _load_inputs below.
"""

_load_outputs = [
    ('kd_tree', 'KDTreeWriter'),
    ('knossos', 'KnossosWriter'),
    ('knossos_legacy', 'LegacyKnossosWriter'),
    ('networkx', 'NXGraphWriter'),
]

_load_inputs = [
    ('bable_instance', 'BableReader'),
    ('knossos', 'KnossosReader'),
    ('networkx', 'NXGraphReader'),
]

writers = dict()
for cur_output_name, cur_output in _load_outputs:
    cur_writer = '%s_writer' % (cur_output, )
    exec('from %s import Writer as %s' % (cur_output, cur_writer, ))
    writers[cur_output_name] = locals()[cur_writer]

readers = dict()
for cur_input_name, cur_input in _load_inputs:
    cur_reader = '%s_reader' % (cur_input, )
    exec('from %s import Reader as %s' % (cur_input, cur_reader, ))
    readers[cur_input_name] = locals()[cur_reader]