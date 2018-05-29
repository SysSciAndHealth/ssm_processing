rlabels2rcodes.py accepts the following three arguments:

1) the path to a file of Responsibilities that have been sorted, i.e., each Responsibility has been assigned an "rcode."

2) a directory of rlabeled SSMs.

3) a directory in which "rcoded" SSMs are to be placed.

This last directory "3)" will contain the output for rlabels2rcodes.py, which is a set of the SSMs that have had all their rlabels replaced by rcodes. An rcode is the code assigned to any Responsibility that is connected to a node (shape) in the sorting process (discussed in "1)" above).

Rcodes are similar to rlabels, with these distinctions: 

An rlabel is surrounded by [square brackets], contains the letter 'r' followed by the integer id of the Responsibility node in the originating SSM, followed by a space and then either the map id (if it's in the SSM name) or the name of the originating SSM. So, for example, an rlabel for the Responsibility with id 7 in an SSM named "testX.json"  would be [r7 testX]. 

However, the rcode for that same Responsibility node would be surrounded by {curly braces}, would begin with "rcode " ("rcode" followed by a single space) and then the actual code that has been assigned to that Responsibility. So if that Responsibility had been sorted so that it was placed under the code "Experimental" then the rcode for it would be {rcode Experimental}.

When the files of node text items (other than Responsibility nodes) are sorted, that activity is to be informed not by rlabels, but by the attached rcodes that have replaced the rlabels. Note that there are multiple rcodes attached to some nodes, just as there were multiple rlabels attached previously. Our intent is that now the rcodes will provide sufficient information -- they contain the actually codes for each connected Responsibility node -- that the analyst who performs the coding operation will be able to make a fully informed choice as to the appropriate code to assign to each node, based on the rcode[s] assigned to it. 

The Responsibility nodes should not need to be sorted again. They've already had codes assigned in the previous sorting process. 
