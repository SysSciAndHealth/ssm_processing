<h3>create_code_matrices.py</h3>

Usage:
* create_code_matrices.py cblm_dir code_matrix_dir

Assumes that the files in the two directories follow this naming convention:
* (cblm) coded binary link matrix: "*name*-CBLM.csv"
* code matrix: "*name*-CM.csv"

where *name* is a string that may or may not be constructed according to a convention defined in https://github.com/steve9000gi/extractMaps/blob/master/README.md.


<h3>create_code_presence_matrix.py</h3>

Generate a matrix where the row names are the names of all the System Support Map files in a project, and the column names are all the "codes" (node text category names) for that project, and each element is the number of times a code appears in the corresponding file.

Usage:

* create_code_presence_matrix.py cblm_dir output_dir

Args:
* cblm_dir: A directory of Coded Binary Link Matrix (CBLM) files.
* output_dir: A directory (required to exist) where the code presence matrix is going to be put.

Requires that the files in cblm_dir follow this naming convention:
* CBLM file: "*name*-CBLM.csv"

where *name* is a string that may or may not be constructed according to a convention defined in https://github.com/steve9000gi/extractMaps/blob/master/README.md.

<h3>CMs_to_3cols.py</h3>

Reads in a directory of code matrices (CMs). Outputs a directory of "3cols," which are 2D arrays, each arranged in three columns, thusly:

<table>
<tr>
<th>from</th>
<th>to</th>
<th>value</th>
</tr>
</table>

where "from" and "to" are codes, and "value" is the number of edges in the originating set of SSMs that go from "from" to "to." In each 3col file output there is a row for each element in its corresponding CM.

Usage:
* CMs_to_3cols.py cm_dir output_dir

Args:

* cm_dir: A directory of Code Matrix (CM) files.
* output_dir: A directory (required to exist) that is the intended target location for a set of "3col" files.

Requires that the files in the two directories follow these naming conventions:

* CM file: "*name*-CM.csv"
* 3col file: "*name*-3col.csv"
