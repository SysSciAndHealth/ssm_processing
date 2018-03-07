#!/usr/bin/env python

""" monodirectionalize_SSM_edges.py.  Read in a set (a directory) of System
    Support Maps (SSMs). For each map, create another map that's identical
    except that the direction of all the inward-pointing arrows is flipped 
    so that all arrows point outwards. Assumption: that all arrows from Role
    and Responsibility nodes point outward, and all other arrows point 
    inward.

    Usage:
        monodirectionalize_SSM_edges.py indir outdir

    Args:
        indir: String path to a directory of System Support Map (SSM) files.
            Expects the files to be in SSM JSON format and end with extension
            ".json"..
        outdir: String path to a directory that is the intended target location
            for a set of rlinked ssm files. If outdir doesn't exist, a
            reasonable attempt will be made to create it.
"""

import sys
import os
import json


def print_node(n):
    if n is not None:
        for k, v in n.iteritems():
            print(k, v)
    else:
        print None


def print_nodes(nodes, num):
    for i in range(0, num):
        n = get_node(i, nodes)
        print "------\nnode #" + str(i)
        print_node(n)


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


def build_monodirectionalized_ssm_path_list(ssm_files, out_dir):
    """ Builds a list of full paths to a set of monodirectionalized SSM files.

    Args:
        ssm_files: A list of SSM filenames, used as the basis for creating
            monodirectionalized SSM filenames.
        out_dir: Path to a directory into which monodirectionalized SSM files
            are intended to go.
    
    Returns:
       A list of full paths to monodirectionalized SSM files.
    """
    out_files = []
    for fname in ssm_files:
        if fname.endswith(".json") or fname.endswith(".JSON"):
            out_path = out_dir + "/" + fname[:-5] + "-monodir.json"
            out_files.append(out_path)
        else:
            print ("build_monodirectionalized_ssm_path_list: non-standard " +
                   "input file name: " + fname)
    return out_files


def print_list(list, title):
    i = 0
    width = 3
    print "\n" + title + ":\n"
    for item in list:
        print "%s. %s" % (str(i).rjust(width), item)
        i += 1


def get_node(id, nodes):
    for n in nodes:
        if n["id"] == id:
            return n
    return None


def monodirectionalize_single_ssm(inpath, outpath):
    """ Open the SSM file located at "inpath". Read it into a dict. Find all
        Wish (star-shaped) and Resource (ellipsoidal) nodes. For each, find all
        links whose source is that node, and in each of those links switch the
        values for "source" and "target". Write the monodirectionalized dict as
        an SSM to outpath.

        Assumes that links for Wishes and Resources always point inwards, and 
        that all other links point outwards.

        Args:
            inpath: full path to an SSM file to be monodirectionalized.
            outpath: full path to an SSM file that will be the
                monodirectionalized equivalent of the SSM at inpath.

        Returns:
            None
    """
    with open(inpath) as json_input_file:
        json_object = json.load(json_input_file)
    json_object = convert(json_object)
    links = json_object["links"]
    nodes = json_object["nodes"]
    print ("inpath: " + inpath + "; " + str(len(links)) + " links; " +
           str(len(nodes)) + " nodes")
    for link in links:
        source_id = link["source"]
        print "source_id: " + str(source_id)
        source_node = [node for node in nodes if node["id"] == source_id][0]
        if source_node["shape"] in ["star", "ellipse"]:
            temp = link["source"]
            link["source"] = link["target"]
            link["target"] = temp
    with open(outpath, "w") as outfile:
        json.dump(json_object, outfile)


def main():
    if len(sys.argv) < 3:
        print ("usage: monodirectionalize_SSM_edges.py indir outdir")
        return
    indir = sys.argv[1]
    outdir = sys.argv[2]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        print "Created " + outdir
    infiles = get_file_list(indir, ".json")
    inpathlist = build_path_list(indir, infiles)
    outpathlist = build_monodirectionalized_ssm_path_list(infiles, outdir)
    for i, inpath in enumerate(inpathlist):
        monodirectionalize_single_ssm(inpath, outpathlist[i])


if __name__ == "__main__":
    main()
