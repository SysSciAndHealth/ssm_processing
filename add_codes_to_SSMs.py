#!/usr/bin/env python

""" add_codes_to_SSMs.py: Add the code for each node in each file in a
        directory of Coded Binary Link Matrices (CBLMs) to each corresponding
	node in each file in a directory of SSM .JSON files in a directory of
	System Support Maps (SSMs), and writes the results to a directory of 
	files of Coded SSMs (CSSMs).

    Usage:
    ./add_codes_to_SSMs.py ssm_dir cblm_dir cssm_dir

    Assumes that each SSM in ssm_dir has a corresponding CBLM file in cblm_dir,
    and that the files for all three directories follow this naming convention:
        SSM : "<name>.json"
        CBLM: "<name>-CBLM.csv"
        CSSM: "<name>-C.json"
    where <name> is a string that may or may not be constructed according to a
    convention defined in
    https://github.com/steve9000gi/extractMaps/blob/master/README.md.
"""

import sys
import os
import json
import re
import ntpath

ssm_dir = sys.argv[1]
cblm_dir = sys.argv[2]
cssm_dir = sys.argv[3]

def add_codes_to_single_ssm(ssm, cblm, cssm_dir):
    with open(ssm) as json_input_file:
        json_object = json.load(json_input_file)

    nodes = json_object["nodes"]
    print 'ssm: ' + ssm + '; cblm: ' + cblm + "; " + str(len(nodes)) + " nodes"

    with open(cblm) as cblm_file: # Read CBLM file as list, each item a row:
        rows = cblm_file.read().split("\n");

    clist = []
    for row in rows: # clist becomes a list of sublists, each sublist a row
        r = row.split("\t") # Split each row into a list of items
        clist.append(r)
    clist.pop() # get rid of empty last row

    node_id_index = 1 # position for NodeID column in CBLM
    code_index = 4    # position for Code column in CBLM

    for c_node_line in clist[1:]: # Skipping headers, select each row
        # Find which node in json object nodes has the same id  as the NodeID in
	# the current c_node_line:
	for j_ix, j_node in enumerate(nodes): # Look at each node in json object
	    if str(j_node["id"]) == c_node_line[node_id_index]:
		j_node["code"] = c_node_line[code_index] # Add matching code
		break

    # Finally, write the json object with codes added to file:
    outfilename = (cssm_dir + "/" + os.path.splitext(ntpath.basename(ssm))[0]
	        + "-C.json")
    print outfilename
    with open(outfilename, "w") as outfile:
	json.dump(json_object, outfile)

# main
ssm_files = []
ssm_files += [fn for fn in os.listdir(ssm_dir) if fn.endswith(".json")]

cblm_files = []
cblm_files += [fn for fn in os.listdir(cblm_dir) if fn.endswith("-CBLM.csv")]

print str(len(ssm_files)) + " =?= " + str(len(cblm_files)) # 1 CBLM for each SSM

for i, ssm in enumerate(ssm_files):
    ssm_path = ssm_dir + "/" + ssm
    cblm_path = cblm_dir + "/" + cblm_files[i]
    add_codes_to_single_ssm(ssm_path, cblm_path, cssm_dir)
