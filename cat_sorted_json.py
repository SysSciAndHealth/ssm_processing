#!/usr/bin/env python

""" cat_sorted_json.py: concatenate a set of System Support Map-derived
    JSON files that represent per-ring sorted output from 
    http://syssci.renci.org/sort.

    Usage:
        cat_sorted_json.py sorted_json_dir


    Argument:
        sorted_jsor_dir: full path to a directory that contains all the 
	.json files to be concatentated. 
"""

import sys
import os
import collections
import json
import string
import psycopg2


def get_file_list(dir):
    """ Get a list of all the .json files in a directory.
    Arg:
        dir: the path to a directory that contains JSON files.
    Returns:
        a list of JSON files in that directory.
    """

    files = []
    files += [fn for fn in os.listdir(dir) if fn.endswith('.json')]
    return files


def build_path_list(dir, file_list):
    """ Builds a list of full paths to a set of CBLM files.
    """
    return [dir + "/" + filename for filename in file_list]


def cat_files(path_list):
    out = {}
    out["sorted"] = []
    for path in path_list:
        #print(path)
        with open(path) as json_data:
            d = json.load(json_data)
            curr_sorted = d["sorted"]
        #print(curr_sorted)
        out["sorted"].extend(curr_sorted)
    return out


def main():
    dir = sys.argv[1]
    file_list = get_file_list(dir)
    path_list = build_path_list(dir, file_list)
    #print str(path_list)
    jsonOut = cat_files(path_list)
    #print(json.dumps(jsonOut))
    outfilepath = dir + "/cattedJSON.json"
    with open(outfilepath, 'w') as outfile:
        json.dump(jsonOut, outfile)
    print "done."


if __name__ == "__main__":
    main()
