#!/home/anaconda/anaconda2/bin/python
import sys
import json
print "Number of arguments: ", len(sys.argv)
with open(sys.argv[1], 'r') as handle:
    parsed = json.load(handle)
    if (len(sys.argv) == 2):
       print(json.dumps(parsed, indent=4, sort_keys=True))
    elif (len(sys.argv) == 3):
       outputFile = open(sys.argv[2], 'w+')
       outputFile.write(json.dumps(parsed, indent=4, sort_keys=True))
    else:
       print(sys.argv[0] + " argument 1: file to pretty print, argument 2: optional output file")
