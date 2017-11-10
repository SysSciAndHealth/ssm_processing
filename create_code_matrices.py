#!/usr/bin/env python

""" create_code_matrices.py

    Usage:
        create_code_matrices.py cblm_dir code_matrix_dir

    Args:
        cblm_dir: A directory of Coded Binary Link Matrix (CBLM) files.
        code_matrix_dir: A directory (required to exist) where a set of Code
            Matrix (CM) files is going to be put.

    Requires that the files in the two directories follow these naming
    conventions:
        CBLM file: "<name>-CBLM.csv"
        CM file: "<name>-CM.csv"
    where <name> is a string that may or may not be constructed according to a
    convention defined in
    https://github.com/steve9000gi/extractMaps/blob/master/README.md.
"""


import sys
import os
import csv
import numpy as np
import pandas as pd


def create_code_list(cblm_files):
    """ Create a list of all the codes in a set of CBLM files.

    Arg:
        cblm_files: List of paths to a set of CBLM files.

    Returns:
        A list of all the codes in those files (duplicates are not only ok but
       expected)..
    """
    clist = []
    for cblm in cblm_files:
        with open(cblm, 'rb') as file_obj:
            reader = csv.reader(file_obj, delimiter='\t')
            next(reader, None) # skip headers
            for row in reader:
                clist.append(row[4])
    return clist


def get_cblm_file_list(cblm_dir):
    """ Get a list of all the CBLM files in a directory.

    Arg:
        cblm_dir: the path to a directory that contains CBLM files.

    Returns:
        a list of CBLM files in that directory.
    """

    cblm_files = []
    cblm_files += [fn for fn in os.listdir(cblm_dir) if fn.endswith('-CBLM.csv')]
    return cblm_files


def build_cblm_path_list(cblm_dir, cblm_file_list):
    """ Builds a list of full paths to a set of CBLM files.
    """
    return [cblm_dir + "/" + filename for filename in cblm_file_list]


def build_cm_path_list(cblm_files, cm_dir):
    """ Builds a list of full paths to a set of CM files. An error message is
        printed to stdout for any file that doesn't follow the CM file naming
        convention.

    Args:
       cblm_files: A list of CBLM filenames, used as the basis for creating CM
           filenames.
       cm_dir: The path of a directory into which CM files are intended to go.

    Returns:
       A list of full paths to CM files.
    """
    cm_files = []
    for cblm_fname in cblm_files:
        if cblm_fname.endswith("-CBLM.csv"):
            cm_path = cm_dir + "/" + cblm_fname[:-7] + "M.csv"
            cm_files.append(cm_path)
        else:
            print "build_cm_file_list: invalid CBLM file name" + cblm_fname
    return cm_files


def initialize_data_frame(code_list):
    """ Construct 2D square data frame with dimensions = length of code_list and
        all elements 0.
    """
    dim = len(code_list)
    temp = np.zeros((dim, dim), dtype=np.int16)
    return pd.DataFrame(temp, columns=code_list, index=code_list,
	dtype=np.int16)


def populate_df(cblm, df_template, master_code_list):
    """ For each row in the cblm, get the code, find out which nodes the current
        node is linked to, find out the codes for each of those, and add 1 to
        the values in the two locations (we're treating edges as non- or bi-
        directional) in the data frame that corresponds to those two codes.

    Args:
        cblm: The full path to a CBLM file that's used as the source for the
            node names and codes that will be used to populate a particular
            Pandas DataFrame.
        df_template: A Pandas DataFrame that's the right size, has the correct
            labels for both rows and columns, but all of whose elements are
            integers = 0.
        master_code_list: A list of all the unique codes in the originating set
            of CBLM files.

    Returns:
        A Pandas DataFrame that represents the connectivity between nodes in an
        SSM, where node names have been replaced by the codes associated with
        them in the file represented by the cblm arg.
    """
    popd_df = df_template.copy()
    #print "About to read " + cblm
    cblm_df = pd.read_csv(cblm, sep='\t')
    curr_code_list = cblm_df["Code"].values.tolist()
    blm = cblm_df.ix[:, 7:] # from first column of adjacency matrix ("blm")
    for i, row in blm.iterrows():
        rlist = row.values.tolist() # sequential indices, not nodeID col labels
        for j, elt in enumerate(rlist):
            if elt != 0:
                row = master_code_list.index(curr_code_list[j])
                col = master_code_list.index(curr_code_list[i])
                popd_df.iloc[row, col] += 1
    return popd_df


def write_code_matrix(file_path, populated_df, code_list):
    """ Write the contents of populated data frame populated_df to file at
        location file_path. Assumes that those row and column labels are the
	appropriate codes.

    Args:
        file_path: The full path to a file to which the code matrix is to be
            written.
        populated_df: A Pandas DataFrame that has been populated by integer
            values representing links between nodes according to the codes
            assigned to those nodes.
        code_list: A list of all the codes represented in populated_df, and
            in the same order.

    Returns:
        None
    """
    with open(file_path, 'w') as file_obj:
        populated_df.to_csv(path_or_buf=file_obj, sep='\t')


def write_code_matrices(cblm_paths, cm_paths, df_template, code_list):
    """ Write out a set of CM files, each of which corresponds to one of the
        CBLM files represented by a set of paths to CBLM files. Also sum all
        the CMs and write the results to the same directory.

    Args:
        cblm_paths: A list of the full paths to a set of CBLM files.
        cm_paths: A list of full paths to which CM files are to be written.
        df_template: A Pandas DataFrame formatted just like the final CM files
            except all the element values are 0.
        code_list: A list of all the codes that are to be immortalized in this
            collection of CM files.

    Returns:
        None
    """
    sum_df = df_template.copy()
    for i, cblm_path in enumerate(cblm_paths):
        popd_df = populate_df(cblm_path, df_template, code_list)
        write_code_matrix(cm_paths[i], popd_df, code_list)
        sum_df = sum_df.add(popd_df, fill_value=-1)
        print str(i) + ': ' + cblm_path + ' -> ' + cm_paths[i]
    if cm_paths:
        write_code_matrix(os.path.dirname(cm_paths[0]) + "/sum-CM.csv",
                          sum_df, code_list)


def main():
    cblm_dir = sys.argv[1]
    code_matrix_dir = sys.argv[2]
    cblm_file_list = get_cblm_file_list(cblm_dir)
    cblm_path_list = build_cblm_path_list(cblm_dir, cblm_file_list)
    code_list = sorted(set(create_code_list(cblm_path_list)))
    cm_path_list = build_cm_path_list(cblm_file_list, code_matrix_dir)
    df_template = initialize_data_frame(code_list)
    write_code_matrices(cblm_path_list, cm_path_list, df_template, code_list)


if __name__ == "__main__":
    main()
