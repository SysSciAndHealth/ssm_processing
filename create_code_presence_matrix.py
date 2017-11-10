#!/usr/bin/env python

""" create_code_presence_matrix.py

    Generate a matrix where the row names are the names of all the System
    Support Map files in a project, and the column names are all the "codes"
    (node text category names) for that project, and each element is the number
    of times a code appears in the corresponding file.

    Usage:
        create_code_presence_matrix.py cblm_dir output_dir

    Args:
        cblm_dir: A directory of Coded Binary Link Matrix (CBLM) files.
        output_dir: A directory (required to exist) where the code presence
            matrix is going to be put.

    Requires that the files in cblm_dir follow this naming convention:
        CBLM file: "<name>-CBLM.csv"
    where <name> is a string that may or may not be constructed according to a
    convention defined in
    https://github.com/steve9000gi/extractMaps/blob/master/README.md.
"""

import sys
import os
import csv
import numpy as np
import pandas as pd
from create_code_matrices import get_cblm_file_list, build_cblm_path_list, \
    create_code_list


def rchop(thestring, ending):
    """ https://stackoverflow.com/questions/3663450/python-remove-substring-only-at-the-end-of-string
    """
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring


def generate_row_names(file_list):
    """ Assumes that file_list is a list of CBLM files. Strip off the file-
        type-specific characters at the end of each and leave the substrings
        uniquely identifying and linking each file sequence (i.e., <name> in
        "<name>[SSM].json" -> "<name>-BLM.csv" -> "<name>-CBLM.csv" ->
        "<name>-CM.csv") within the current project.
    """
    return [rchop(file_name, "-CBLM.csv") for file_name in file_list]


def initialize_data_frame(file_list, code_list):
    """ Construct 2D data frame where rows are system support map file names
        and columns are codes; all elements 0.
    """
    row_names = generate_row_names(file_list)
    n_rows = len(row_names)
    n_cols = len(code_list)
    temp = np.zeros((n_rows, n_cols), dtype=np.int16)
    return pd.DataFrame(temp, columns=code_list, index=row_names,
                        dtype=np.int16)


def populate_df(cblms, codes, df_template):
    """ For each Coded Binary Link Matrix (CBLM) file in cblms, find out how
        often each code is used, and put that number in the element with row
        corresponding to the cblm currently under consideration and with column
        corresponding to that code.

    Args:
        cblms: A list of full paths to a set of CBLM files.
            the codes that will be used to populate a particular
            Pandas DataFrame.
        codes: A list of all the unique codes in the originating set
            of CBLM files.
        df_template: A Pandas DataFrame that's the right size, has the correct
            labels for both rows and columns, but all of whose elements are
            integers = 0.

    Returns:
        A Pandas DataFrame that represents how many times each code is used in
        each file.
"""
    df = df_template.copy()
    for row, cblm in enumerate(cblms):
        cblm_df = pd.read_csv(cblm, sep='\t')
        curr_code_list = cblm_df["Code"].values.tolist()
        # print str(row) + ": " + str(curr_code_list) + "\n"
        for col, code in enumerate(curr_code_list):
            df.iloc[row, df.columns.get_loc(code)] += 1
    return df


def write_matrix(df, output_path):
    """ Write contents of dataFrame df to output_path/CodePresenceMatrix.csv.
    """
    #  2do: Handle possible trailing "/" in output_path.
    file_path = output_path + "/CodePresenceMatrix.csv"
    with open(file_path, 'w') as file_obj:
        df.to_csv(path_or_buf=file_obj, sep='\t')


def main():
    cblm_dir = sys.argv[1]
    output_path = sys.argv[2]
    cblm_file_list = get_cblm_file_list(cblm_dir)
    cblm_path_list = build_cblm_path_list(cblm_dir, cblm_file_list)
    code_list = sorted(set(create_code_list(cblm_path_list)))

    # print "cblm_file_list: " + str(cblm_file_list)
    # print "cblm_path_list: " + str(cblm_path_list)
    # print "code_list: " + str(code_list)

    df_template = initialize_data_frame(cblm_file_list, code_list)
    df = populate_df(cblm_path_list, code_list, df_template)
    # print df.to_string()
    write_matrix(df, output_path)
    print "Done."

if __name__ == "__main__":
    main()
