#!/usr/bin/env python

""" add_rlabels_to_SSMs.py. An "rlabel" is a string that uniquely identifies
    a Responsibility node in the context of a set (a directory) of System 
    Support Maps (SSMs).

    Approach

    Treat each Responsbility node as the root of a graph comprised of all the 
    nodes that are linked to it in the SSM to which it belongs. Traverse that
    graph, attaching to each node the rlabel that uniquely identifies the root
    Responsibility. 
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
    """ https://stackoverflow.com/questions/13101653/python-convert-complex-dictionary-of-strings-from-unicode-to-ascii
    """
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def mark_nodes_unvisited(nodes):
    for n in nodes:
        n["visited"] = False


def init_rlabel_lists(nodes):
    for n in nodes:
        if "rlabels" not in n:
            n["rlabels"] = []


def get_role(nodes):
    for n in nodes:
        if n["type"] == "role":
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
    resp = []
    for n in nodes:
        if n["type"] == "responsibility":
          resp.append(n)
    return resp


def build_rlabel(fname, r_id):
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


def traverse_rgraph(links, nodes, r, resp, fname):
    """ For a given responsibility node r traverse the subgraph of nodes that
        are connected to r, marking each as visited and appending the 
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
            nodes: the nodes subdict from the current SSM.
            r: the responsbility node whose subgraph we're traversing.
            resp: list of responsibility nodes: all need to be marked as
                "visited."
            fname: name of the SSM file from which these various elements have
                been extracted.
        Returns:
            None
    """
    r_id = r["id"]
    rlabel = build_rlabel(fname, r_id)
    init_visitation(nodes, resp)
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
    init_visitation(nodes, resp)
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


def add_rlabels_to_single_ssm(inpath):
    """ Open the SSM file located at "inpath". Read it into a dict. Find all
        Responsibility nodes. For each Responsibility, append an rlabel which
        uniquely identifies that Responsibility to the "name" value of every
        node connected to that Responsibility.  Write the rlabeled dict as an
	SSM to a .json file.

        Arg: 
            inpath: full path to an SSM file to be rlabeled.

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
    resp = get_responsibilities(nodes)
    print str(len(resp)) + " responsibility nodes"
    for n, r in enumerate(resp):
        print ("resp #" + str(n) + "; id: " + str(r["id"]) + "; name: \"" +
               r["name"] + "\"")
        traverse_rgraph(links, nodes, r, resp, ntpath.basename(inpath))
    print_nodes(nodes, 30)
    outpath = build_outpath(inpath)
    print outpath
    with open(outpath, "w") as outfile:
        json.dump(json_object, outfile)


def main():
    if len(sys.argv) < 2:
        print "usage: add_rlabels_to_SSMs.py inpath use_full_filename"
        return
    inpath = sys.argv[1]
    use_full_filename = False
    if len(sys.argv) > 2 and sys.argv[2] in ['t', 'T', "TRUE", "true", "True"]:
        use_full_filename = True
 #   print "add_rlabels_to_SSMs.py: inpath = \"" + inpath + "\" " + str(use_full_filename)

    add_rlabels_to_single_ssm(inpath)


if __name__ == "__main__":
    main()
