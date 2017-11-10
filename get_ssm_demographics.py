#!/usr/bin/env python

""" get_ssm_demographics.py: Read a directory of ssms, write out their
    demographic info to a csv file called demographics.csv.

    Usage:
        get_ssm_demographics.py in_dir

"""

import sys
import os
import collections
import json
import string
import re
import ntpath

def main():
    in_dir = sys.argv[1]
    print "get_ssm_demographics.py " + in_dir

    ssm_files = []
    ssm_files += [fn for fn in os.listdir(in_dir) if fn.endswith(".json")]
    out_path = in_dir + "/demographics.csv"
    outf = open(out_path, "w")
    outf.write("File Name\tCounty or Municipality\tRace\tHispanic?\tLanguage\tChild's Age\tInsurance\tHealth Conditions\n")
    for i, ssm in enumerate(ssm_files):
        ssm_path = in_dir + "/" + ssm
        with open(ssm) as json_input_file:
            map = json.load(json_input_file)
            outf.write(ssm + "\t" + map["county"] + "\t" + ''.join(map["race"]) + "\t" + str(map["hispanic"]) + "\t" + map["language"] + "\t" + map["age"] + "\t" + map["insurance"] + "\t" + ''.join(map["healthConditions"]) + "\n")

if __name__ == "__main__":
    main()
