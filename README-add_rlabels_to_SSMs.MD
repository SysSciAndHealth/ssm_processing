As I conceive it, an example that tags something like "r37-1056 " at the end of a node text string is just that: a node text string, and *not* a code or any part of a code. These tags (I guess I'm calling them "r-labels," although that's not a great name, but it distinguishes them from other entities that might be called tags or codes or other widely used terms) would provide information to analysts in the list of node text items to be sorted so they know exactly what responsibility each node text item is attached to. They would then use that information to determine whether they want to create multiple codes for node text items that in themselves look identical but may be associated with different Responsibilities and/or in different maps. I don't see any way to preserve analysts from having to make the key decisions about whether or not two node text items get grouped together under a single code or whether they need to be categorized under different codes because they're connected to semantically different Responsibilities. Here's an example:

As it is now an analyst might get a list of items to be coded that includes the following:

...
RESPONSIBILITIES:
...
child's health
child's education
child's education
...
NEEDS:
...
money
money
money
...

and they analyst would now conclude that all three "money" node text items belong under a single code, say "Money Needs".

I'm proposing that in the future they'd get this instead:
 
...
RESPONSIBILITIES:
...
child's health r26-1234
child's education r23-1234
child's education r11-1196
...
NEEDS:
...
money r26-1234
money r23-1234
money r11-1196
...

This would mean that:
the first "money" node text item is attached to a Responsibility with node id 26 in the SSM with id 1234
the second "money" node text item is attached to a Responsibility with node id 23 in the SSM with id 1234. It's in the same SSM but attached to a different Responsibility and thus might or might not be coded differently, depending on the text for the Responsibility node[s] involved. 
the third "money" node text item is attached to a Responsibility with node id 11 in SSM with id 1196: different node, different SSM. 
 
So the analyst would look at the first "money" node text item and see that it's associated with Responsibility r26-1234 ("...health") and would choose to place it under some code like "Child's Health Care Need."

The analyst would look at the second "money" text item and see that it's associated with Responsibility r23-1234 ("...education"). Although the node text is identical to that of the preceding, it's associated with a different Responsibility that would indicate a different coding, say "Child's Education Need."

For the third node text item the analyst would look at the associated Responsibility -- child's education r11-1196 -- and conclude that it should also be coded under "Child's Education Need," even though it's not only associated with a different Responsibility but that it's from a different SSM. However, although the actual Responsibility node is different (it's in a different SSM) it's semantically similar (in this case identical) to the Responsibility with r-label r23-1234, so it would belong under the same code. That would be the analyst's judgment call, easy here because the two Responsibilities (r23-1234 and r11-1196​) have identical text, but it may not always be so obvious. 

Note that the RESPONSIBILITY node text items have their own "r-labels" attached so that the analyst can look them up by r-label to determine how to code all the other  associated node text items. 

ROLE node text items wouldn't get r-labels. Neither, of course, would text from any nodes that aren't attached to any Responsibilities. 

If a node is attached to multiple Responsibilities, I guess it gets multiple r-labels, one for each. How does the analyst handle such an eventuality? I guess it will be a judgement call. 

Analysts would be free to put whatever additional tags or labels they want into their codes, but the software (Python script) I'm working on would not do *anything* to the codes. It would just add "r-labels" to the various node text items to be sorted, as guides for the analysts in their coding process.

Senior Research Software Develope
Renaissance Computing Institute (RENCI)
University of North Carolina at Chapel Hill​
Phone: 919-428-4097
Email: stevec@renci.org
