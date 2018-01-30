#!/usr/bin/env python

""" add_rlabels_to_SSMs.py. An "rlabel" is a string that uniquely identifies
    a Responsibility node in the context of a set (a directory) of System 
    Support Maps (SSMs).

    Approach

    Treat each Responsibility node as the root of a graph comprised of all the 
    nodes that are linked to it in the SSM to which it belongs. Traverse that
    graph, attaching to each node the rlabel that uniquely identifies the root
    Responsibility. 

    Usage:
        add_rlabels_to_SSMs.py indir outdir [use_full_filename]

    Args:
        indir: A directory of System Support Map (SSM) files. Expects the files
            to be in JSON format and end with extension ".json."
        outdir: A directory that is the intended target location for a set of 
            rlinked ssm files. If outdir doesn't exist, a reasonable attempt 
            will be made to create it.
        use_full_filename (optional): Boolean. If true, create rlabel using 
            the whole input SSM filename (excepting the ".json" extension).
            False is the default, in which case the SSM filename is expected to
            have the form "text<database id>.json, where <database id is the
            SSM's id in the server PostgreSQL database.
"""

import sys
import os
import json
import re
import ntpath
import Queue


def print_node(n):
    if n != None:
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


def build_rlabeled_ssm_path_list(ssm_files, out_dir):
    """ Builds a list of full paths to a set of rlabeled SSM files. 
    Args:
        ssm_files: A list of SSM filenames, used as the basis for creating
            rlabeled SSM filenames.
        out_dir: Path to a directory into which rlabeled SSM files are intended
            to go.
    Returns:
       A list of full paths to rlabeled SSM files.
    """
    out_files = []
    for fname in ssm_files:
        if fname.endswith(".json") or fname.endswith(".JSON"):
            out_path = out_dir + "/" + fname[:-5] + "-rlabeled.json"
            out_files.append(out_path)
        else:
            print ("build_rlabeled_ssm_path_list: non-standard input file "
                   + "name: " + fname)
    return out_files


def print_list(list, title):
    i = 0
    width = 3
    print "\n" + title + ":\n"
    for item in list:
        print "%s. %s" % (str(i).rjust(width), item)
        i += 1


def mark_nodes_unvisited(nodes):
    for n in nodes:
        n["visited"] = False


def init_rlabel_lists(nodes):
    for n in nodes:
        if "rlabels" not in n:
            n["rlabels"] = []


def get_role(nodes):
    for n in nodes:
        #if n["type"] == "role":
        if n["shape"] == "circle":
            return n
    return None


def init_visitation(nodes, responsibilities):
    mark_nodes_unvisited(nodes)
    role = get_role(nodes)
    if role is not None:
        role["visited"] = True
    for r in responsibilities:
        r["visited"] = True


def get_responsibilities(nodes):
    responsibilities = []
    for n in nodes:
        #if n["type"] == "responsibility":
        if n["shape"] == "rectangle":
          responsibilities.append(n)
    return responsibilities


def build_rlabel(fname, r_id):
    """ The several scripts that extract SSMs from the database build filenames
        that incorporate the SSM's database id into the filename. If that id is 
        present in the filename we'd like to use it (for clarity and
        compactness) in the rlabel. If the id is not in the filename, which has
        occurred for sets of SSMs that we constructed by a researcher and saved
        on a local machine, we use the full filename (with the ".json"
        extension lopped off).

    Args:
        fname: the name of the current SSM file in which the Responsibility node
            currently of interest is to be found.
        r_id: the integer id of that Responsibility node in that SSM.

    Returns:
        an "rlabel" string
    """
    if use_full_filename:
        basename = os.path.basename(fname)
        base = os.path.splitext(basename)[0] 
        return "[r" + str(r_id) + "-" + base + "]"
    else:
        ssm_id = re.findall(r'\d+', fname)[-1]    
        return "[r" + str(r_id) + "-" + ssm_id + "]"


def get_node(id, nodes):
    for n in nodes:
        if n["id"] == id:
            return n
    return None


def get_targets_of(n, links, nodes):
    targets = []
    for l in links:
        if l["source"] == n["id"]:
            targets.append(get_node(l["target"], nodes))
    return targets


def get_sources_of(n, links, nodes):
    sources = []
    for l in links:
        if l["target"] == n["id"]:
            sources.append(get_node(l["source"], nodes))
    return sources


def build_outpath(inpath):
    split_inpath = inpath.rsplit('.', 1)
    return split_inpath[0] + "-rlabeled.json"


def traverse_rgraph(links, nodes, r, responsibilities, fname):
    """ For a given responsibility node r traverse the *directed* subgraph of
        nodes that are connected to r, marking each as visited and appending the
        appropriate rlabel to each of those connected nodes' "name" field.

        See http://www.cs.cornell.edu/courses/cs2112/2012sp/lectures/lec24/lec24-12sp.html: "Breadth-first search"

        frontier = new Queue()
        mark root visited (set root.distance = 0)
        frontier.push(root)
        while frontier not empty {
            Vertex v = frontier.pop()
            for each successor v' of v {
                if v' unvisited {
                    frontier.push(v')
                    mark v' visited (v'.distance = v.distance + 1)
                }
            }
        }

    Args:
        links: the links sub-dict from the current SSM.
        nodes: the nodes sub-dict from the current SSM.
        r: the responsbility node whose subgraph we're traversing.
        responsibilities: list of responsibility nodes: all need to be marked as
            visited to terminate traversal at their positions in the graph.
        fname: name of the SSM file from which these various elements have been
            extracted.

    Returns:
        None
    """
    r_id = r["id"]
    rlabel = build_rlabel(fname, r_id)
    init_visitation(nodes, responsibilities)
    init_rlabel_lists(nodes)

    q = Queue.Queue()
    q.put(r)
    while not q.empty():
        n = q.get()
        newname = n["name"] + " " + rlabel
        n["name"] = newname
        n["rlabels"].append(rlabel)
        targets = get_targets_of(n, links, nodes)
        for t in targets:
            if t["visited"] == False:
                t["visited"] = True;
                q.put(t)

    # Note: this approach isolates the source-to-target links from the target-
    # to-source links, i.e., it doesn't identify connectivity via the 
    # combination, e.g., node[a] -> node[b] <- node[c]: node[a] is connected to
    # node[c] but this won't find it. We need to convert the directed node 
    # representation to an undirected equivalent if the latter is what we wish
    # to capture. 
    init_visitation(nodes, responsibilities)
    q.put(r)
    while not q.empty():
        n = q.get()
        if rlabel not in n["rlabels"]: # avoid duplicating rlabels
            newname = n["name"] + " " + rlabel
            n["name"] = newname
            n["rlabels"].append(rlabel)
        sources = get_sources_of(n, links, nodes)
        for s in sources:
            if s["visited"] == False:
                s["visited"] = True;
                q.put(s)


def build_undirected_adjacency_matrix(num_nodes, links):
    """ Note that if there is a link shown from a source to a target node, there
        is also a link shown from target to source, i.e., m[i, j] == m[j, i].
        It's assumed that redundncies will be handled elsewhere.
    
    """
    m = [[0 for x in range(num_nodes)] for y in range(num_nodes)]
    for l in links:
        s = l["source"]
	t = l["target"]
	m[s][t] = m[t][s] = 1
    return m
    

def traverse_undirected_rgraph(links, nodes, r, responsibilities, fname):
    """ Traverse the subgraph with r at its root as though all links are
        undirected.
       
        NOTE: Placeholder function not yet implemented.

    Args:
        m: undirected adjacency matrix
        (links: the links sub-dict from the current SSM.)?
        nodes: the nodes sub-dict from the current SSM.
        r: the responsbility node whose subgraph we're traversing.
            responsibilities: list of responsibility nodes: all need to be
                marked as "visited."
        fname: name of the SSM file from which these various elements have
                been extracted.

    Returns:
            None
    num_nodes = len(nodes)
    r_id = r["id"]
    rlabel = build_rlabel(fname, r_id)
    init_visitation(nodes, responsibilities)

    q = Queue.Queue()
    q.put(r)
    while not q.empty():
        n = q.get()
        newname = n["name"] + " " + rlabel
        n["name"] = newname
        for i in range(0, num_nodes):
	    for j in range(0, num_nodes):
                if m[i][j] == 1:
                    print "traverse_undirected_rgraph inmost loop"
    """
    r_id = r["id"]
    rlabel = build_rlabel(fname, r_id)
    init_visitation(nodes, responsibilities)
    init_rlabel_lists(nodes)
    
    undirlinks = []
    for l in links:
        undirlinks.append({"source": l["source"], "target": l["target"]})
        undirlinks.append({"source": l["target"], "target": l["source"]})

    q = Queue.Queue()
    q.put(r)
    while not q.empty():
        n = q.get()
        newname = n["name"] + " " + rlabel
        n["name"] = newname
        n["rlabels"].append(rlabel)
        targets = get_targets_of(n, undirlinks, nodes)
        for t in targets:
            if t["visited"] == False:
                t["visited"] = True;
                q.put(t)


def add_rlabels_to_single_ssm(inpath, outpath):
    """ Open the SSM file located at "inpath". Read it into a dict. Find all
        Responsibility nodes. For each Responsibility, append an rlabel which
        uniquely identifies that Responsibility to the "name" value of every
        node connected to that Responsibility.  Write the rlabeled dict as an
        SSM to outpath.

        Args: 
            inpath: full path to an SSM file to be rlabeled.
            outpath: full path to an SSM file that will be the rlabeled 
                equivalent of the SSM at inpath.

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
    responsibilities = get_responsibilities(nodes)
    print str(len(responsibilities)) + " responsibility nodes"
    for n, r in enumerate(responsibilities):
        print ("resp #" + str(n) + "; id: " + str(r["id"]) + "; name: \"" +
               r["name"] + "\"")
        #traverse_rgraph(links, nodes, r, responsibilities,
        #                ntpath.basename(inpath))
        traverse_undirected_rgraph(links, nodes, r, responsibilities,
                                   ntpath.basename(inpath))
    # print_nodes(nodes, 30)
    with open(outpath, "w") as outfile:
        json.dump(json_object, outfile)


use_full_filename = False

def main():
    if len(sys.argv) < 3:
        print "usage: add_rlabels_to_SSMs.py indir outdir [use_full_filename]"
        return
    indir = sys.argv[1]
    outdir = sys.argv[2]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        print "Created " + outdir

    global use_full_filename
    if len(sys.argv) > 3 and sys.argv[3] in ['t', 'T', "TRUE", "true", "True"]:
        use_full_filename = True

 #   print "add_rlabels_to_SSMs.py: inpath = \"" + inpath + "\" " + str(use_full_filename)

#    add_rlabels_to_single_ssm(inpath)
    infiles = get_file_list(indir, ".json")
    inpathlist = build_path_list(indir, infiles)
    build_rlabeled_ssm_path_list(infiles, outdir)
    outpathlist = build_rlabeled_ssm_path_list(infiles, outdir)
    for i, inpath in enumerate(inpathlist):
        add_rlabels_to_single_ssm(inpath, outpathlist[i])

use_full_filename = False

if __name__ == "__main__":
    main()
