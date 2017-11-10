#!/usr/bin/env python

""" CMs_to_3cols.py

    Reads in a directory of code matrices (CMs). Outputs a directory of
    "3cols," which are 2D arrays, each arranged in three columns, thusly:

    from    to   value

    where "from" and "to" are codes, and "value" is the number of edges in the
    originating set of SSMs that go from "from" to "to." In each 3cols file
    output there is a row for each element in its corresponding CM.

    Usage:
        CMs_to_3cols.py cm_dir output_dir [min_val]

    Args:
        cm_dir: A directory of Code Matrix (CM) files.
        output_dir: A directory (required to exist) that is the intended target
            location for a set of "3cols" files.
        min_val (optional): the minimum value for the int in column 3 below
            which a row will not be printed. Defaults to 0 (all rows printed).

    Requires that the files in the two directories follow these naming
    conventions ("get" stands for "greater or equal to"):
        CM file: "<name>-CM.csv"
        3cols file: "<name>-3cols_get<min_val>.csv"
"""


import sys
import os
import csv
import numpy as np
import pandas as pd


def get_file_list(dir, suffix):
    """ Get a list of all the files (in "dir") whose names end in "suffix."

    Args:
        dir: the path to a directory.
        suffix: the ending substring used for selecting files.

    Returns:
        a list of files in "dir" ending with "suffix."
    """
    files = []
    files += [fn for fn in os.listdir(dir) if fn.endswith(suffix)]
    return files


def build_path_list(dir, file_list):
    """ Builds a list of full paths to a set of files.
    """
    return [dir + "/" + filename for filename in file_list]


def build_3cols_path_list(cm_files, out_dir, min_val):
    """ Builds a list of full paths to a set of 3cols files. An error
        message is printed to stdout for any file that doesn't follow the
        3cols file naming convention.

    Args:
        cm_files: A list of CM filenames, used as the basis for creating
            3cols filenames.
        out_dir: Path to a directory into which 3cols files are intended to
            go.
        min_val: the minimum value for column 3 below which a line is not
            written to file.

    Returns:
       A list of full paths to 3cols files.
    """
    out_files = []
    for cm_fname in cm_files:
        if cm_fname.endswith("-CM.csv"):
            out_path = (out_dir + "/" + cm_fname[:-6] + "3cols_get" +
                        str(min_val) + ".csv")
            out_files.append(out_path)
        else:
            print "build_3cols_path_list: invalid CM file name " + cm_fname
    return out_files


def print_list(list, title):
    i = 0
    width = 3
    print "\n" + title + ":\n"
    for item in list:
        print "%s. %s" % (str(i).rjust(width), item)
        i += 1


def convert_CM_to_3cols(cm_path, outfile_path, min_val):
    """ Reads a code matrix (CM) file and creates an equivalent 3cols file.

        Args:
            cm_path: Full path to a CM file.
            outfile_path: Full path to which the equivalent 3cols file is to
                be written.
            min_val: the minimum value for the int in the third column. If
                "val" < min_val the line is not printed.

      Returns:
          None
    """
    cm = pd.read_csv(cm_path, delimiter="\t", index_col=0)
    outfile = open(outfile_path, "w")
    outfile.write("From:\tTo:\tValue:\n")
    for row_name, row in cm.iterrows():
        for col_name, value in row.iteritems():
            if value >= int(min_val):
                outfile.write(col_name + "\t" + row_name + "\t" + str(value) +
                              "\n")
    outfile.close()


def convert_CMs_to_3cols(cm_paths, out_paths, min_val):
    """ Write out a set of 3cols files, each of which corresponds to one
        of the CM files represented by a set of paths to CM files.

    Args:
        cm_paths: A list of the full paths to a set of CM files.
        out_paths: A list of full paths to which 3cols files are to be written.
        min_val: the minimum value for column 3 below which a line is not
            written to file.

    Returns:
        None
    """
    for i, cm_path in enumerate(cm_paths):
        print "%s: %s\t->\t%s" % (str(i).rjust(3), cm_path, out_paths[i])
        convert_CM_to_3cols(cm_path, out_paths[i], min_val)


def main():
    if len(sys.argv) < 3:
        print "usage: CMs_to_3cols.py cm_dir output_dir [min_val]"
        return
    cm_dir = sys.argv[1]
    out_dir = sys.argv[2]
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print "Created " + out_dir
    min_val = 0
    if (len(sys.argv) > 3):
        min_val = sys.argv[3]
    cm_file_list = get_file_list(cm_dir, "-CM.csv")
    cm_path_list = build_path_list(cm_dir, cm_file_list)
    out_path_list = build_3cols_path_list(cm_file_list, out_dir, min_val)
    convert_CMs_to_3cols(cm_path_list, out_path_list, min_val)


if __name__ == "__main__":
    main()
