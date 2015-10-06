__author__ = 'Fabian Svara'

from bable.BableAnnotation import BableAnnotation

example_knossos_in_fname = 'knossos_zip_example.k.zip'
scaling = (9., 9., 21.)

ba = BableAnnotation()
ba.info()

# Read from on-disk knossos format
ba.read('knossos', example_knossos_in_fname, scaling=scaling)
print ba

# Write out to on-disk format
#
# Re-write to knossos format
ba.write('knossos', 'example_knossos_output.nml')

# Instead of writing to external files, we can return representations of the
# data as different types of python objects.
#
# Output NetworkX graph of bable Node instances
nx_graph = ba.write('networkx', None)

# Output kd-tree based on kd-tree implementation for scipy.spatial
kd_tree = ba.write('kd_tree', None)

# Output a LegacySkeleton representation
legacy_knossos_skeleton = ba.write('knossos_legacy', None, scaling=scaling)

# We can grow the skeleton represented by BableAnnotation simply by re-using
# the instance and reading again
#

ba.read('knossos', example_knossos_in_fname, scaling=scaling)

# ba now contains the same skeleton twice
print ba




