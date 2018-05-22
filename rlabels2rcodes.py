#!/usr/bin/env python

""" rlabels2rcodes.py

    Assumes that there exists, for a directory of System Support Maps (SSMs), a
    JSON file that contains the all Responsibility node text items from those
    SSMs, sorted by code, and with the same format as output by the "sort"
    online utility (see https://github.com/steve9000gi/sort).

    No rlabels in input? No error, just no rcodes in output. 

    Usage:
        rlabels2rcodes.py path/to/sorted_resp_file
                          rlabeled_ssm_dir
                          rcoded_ssm_dir
    Args:
        sorted_resp_file: file of responsibility node texts, sorted by codes
        rlabeled_ssm_dir: A directory (required to exist) that contains a set of
            rlabeled SSMs.
	rcoded_ssm_dir: an output directory of SSMs, identical to
	    rlabeled_ssm_dir except that every rlabel in every SSM has been
	    replaced by its corresponding rcode.



"""

import sys
import os
import csv
import json
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


def build_rcoded_ssm_path_list(ssm_files, out_dir):
    """ Builds a list of full paths to a set of rcoded SSM files.
    Args:
        ssm_files: A list of SSM filenames, used as the basis for creating
            rcoded SSM filenames.
        out_dir: Path to a directory into which rcoded SSM files are intended
            to go.
    Returns:
       A list of full paths to rcoded SSM files.
    """
    out_files = []
    for fname in ssm_files:
        if fname.endswith(".json") or fname.endswith(".JSON"):
            if fname[:-5].endswith("-rlabeled"):
                out_path = out_dir + "/" + fname[:-14] + "-rcoded.json"
            else:
                out_path = out_dir + "/" + fname[:-5] + "-rlabeled.json"
            out_files.append(out_path)
        else:
            print ("build_rlabeled_ssm_path_list: non-standard input file " +
                   "name: " + fname)
    return out_files


def print_list(list, title):
    i = 0
    width = 3
    print "\n" + title + ":\n"
    for item in list:
        print "%s. %s" % (str(i).rjust(width), item)
        i += 1


def convert(input):
    """ Convenience function to convert from unicode to ascii for easier
        reading of diagnostic output. From https://stackoverflow.com/questions/13101653/python-convert-complex-dictionary-of-strings-from-unicode-to-ascii
    """
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def build_rcode_lookup(rcodepath):
    rcode_lookup = {}
    with open(rcodepath) as f:
        dct = convert(json.load(f))
    print "\nResponsibilities dict:"
    for rlist in dct["sorted"]:
        rcode = rlist["title"]
        rcl = []
        print "rcode: " + rcode
        for ti in rlist["textItems"]:
            rcode_lookup[ti["text"]] = rcode
            print ti["text"]
        print "\n"
    print "\n"
    return rcode_lookup


def open_ssm(inpath):
    ssm = open(inpath).read()
    return convert(json.loads(ssm))


def replace_rlabels_with_rcodes(rcode_lookup, ssm):
    """ Look at the text for each node in ssm. If it has one or more rlabels,
        then replace each rlabel with the corresponding rcode as indicated in
        rcode_lookup.
    
        Args:
            rcode_lookup:
            ssm:
    
        Returns: a system support map identical to ssm except that each rlabel
            has been replaced with its corresponding rcode.
    """
    rcoded_ssm = ssm 
    keys = rcode_lookup.keys()
    print keys
    nodes = rcoded_ssm["nodes"]
    for node in nodes:
        n_rlabels = len(node["rlabels"])
        print "#rlabels: " + str(n_rlabels)
        print "node name: " + node["name"]
        delabeled = node["name"].split(" [r", 1)[0]
        print "delabeled: " + delabeled
        new_name = delabeled
        for rlabel in node["rlabels"]:
            print rlabel
            for key in keys:
                if rlabel in key:
                    rcode = rcode_lookup[key]
                    new_name = new_name + " {rcode " + rcode + "}"
                    break
        node["name"] = new_name
    return rcoded_ssm

    
def write_ssm_to_file(ssm, filepath):
    with open(filepath, "w") as fp:
        json.dump(ssm, fp)


def main():
    if len(sys.argv) < 4:
        print "Missing parameter[s]"
        print ("usage: rlabels2rcodes.py path/to/sorted_resp_file"
               "\n\t\t\t rlabeled_ssm_dir\n\t\t\t rcoded_ssm_dir")
        return
    sorted_resp_file_path = sys.argv[1]
    if not os.path.isfile(sorted_resp_file_path):
        print ("sorted responsibilities file \"" + sorted_resp_file_path +
               "\" not found.")
        return
    rlabeled_ssm_dir = sys.argv[2]
    if not os.path.exists(rlabeled_ssm_dir):
        print "rlabeled_ssm_dir \"" + rlabeled_ssm_dir + "\" not found."
        return
    rcoded_ssm_dir = sys.argv[3]
    if not os.path.exists(rcoded_ssm_dir):
        os.makedirs(rcoded_ssm_dir)
        print "Created " + rcoded_ssm_dir
    infiles = get_file_list(rlabeled_ssm_dir, ".json")
    inpathlist = build_path_list(rlabeled_ssm_dir, infiles)
    outpathlist = build_rcoded_ssm_path_list(infiles, rcoded_ssm_dir)
    rcode_lookup = build_rcode_lookup(sorted_resp_file_path)
    width = 3
    for i, inpath in enumerate(inpathlist):
      print "in:  %s. %s" % (str(i).rjust(width), inpath)
      print "out: %s. %s" % (str(i).rjust(width), outpathlist[i])
      ssm = open_ssm(inpath)
      rcoded_ssm = replace_rlabels_with_rcodes(rcode_lookup, ssm)
      write_ssm_to_file(rcoded_ssm, outpathlist[i])


if __name__ == "__main__":
      main()
