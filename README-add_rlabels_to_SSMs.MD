<h1>README: add_rlabels_to_SSMs<h1>

<p>First, every Responsibility in every SSM file in the input directory is identified and assigned an rlabel, as follows: "[r" + <responsibility node id> + "-" + <SSM database id> + "]".  This uniquely identifies every Responsibility in the input directory of SSMs. For instance, looking in aggregated.txt (it's in the attached blm-rlabeled.zip file), I see the text "Academic/classroom support" from the Responsibility node with id = 5 in the SSM with database id = 1008. My script has created an rlabel "[r5-1008]": it's the only responsibility in the whole directory with that rlabel. So the rlabel is appended to the text with this result: "Academic/classroom support [r5-1008]". That rlabel is now attached to that Responsibility's node text if you open up the rlabeled SSM, it's in the BLM generated from map 1008, and it's in the lists of node texts to be sorted, both in RESPONSIBILITIES.txt and aggregated.txt (the latter file simply being the concatenation of all the files of node texts to be sorted that have been separated by ring).</p>

<p>Next, the script does a graph traversal from each of those Responsibility nodes, tracking every connection *from* a source (Responsibility) *to* a target node until each of those nodes has had attached to its text that same rlabel for the Responsibility node at the root of the graph. Because of your arrow directionality conventions, this means that it will primarily be Need nodes that are so labeled (Responsibilities point to Needs; most other node types, when they're connected to a Responsibility, points *to* it).</p> 

<p>We still need to confirm which kinds of nodes are most susceptible to the "source ambiguity" problem she identified. According to my notes from our meeting with analyst Shaghayegh Arangdad on 10/11/18, the main concern was with distinguishing whether it's one or multiple Responsibility nodes that are connected to multiple identical Needs. If this is indeed the case, then I think this approach might take care of it. More later about undirected graph traversals.</p>

<p>Here's a real-world example aggregated.txt (or NEEDS.txt), both in the attached files. There are these two (originally identical) node text items in the NEEDS list:
<ul>
<li>time commitment [r4-1000]</li>
<li>time commitment [r5-1000]</li>
</ul>
I think this is what Shaghayegh was referring to. Without the appended rlabels these two items would be indistinguishable and would probably both be coded the same. However, we see from the rlabels that the first is connected to the Responsibility with id = 4  and the second to the Responsibility with id = 5 from the SSM with database id 1000. The sorting analyst can look under RESPONSIBILITIES and find the corresponding node texts: 
<ul>
<li>County Fiscal Team for Special Children's Services division [r4-1000]</li>
<li>Early Intervention Coordinating Council participant [r5-1000]</li>
</ul>
Those could very well require different codes, and the analyst now has the info (via rlabel) to decide whether to assign each the same or a different code. These two identical Responsibility nodes happen to be from the same SSM, but this whole process should apply just as well if they come from different maps. We've probably seen this more than once with needs like "time" or "money".,/p>

<h3>A more generic example</h3>
<p>An analyst might get a list of items to be coded that includes the following:

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

and without additional information the analyst would now conclude that all three "money" node text items belong under a single code, say "Money Needs".

<p>Rlabeling would provide this information:
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
</p>

<p>This would mean that:

<ul>
<li>The first "money" node text item is attached to a Responsibility with node id 26 in the SSM with id 1234.</li>
<li>The second "money" node text item is attached to a Responsibility with node id 23 in the SSM with id 1234. It's in the same SSM but attached to a different Responsibility and thus might or might not be coded differently, depending on the text for the Responsibility node[s] involved.</li>
<li>The third "money" node text item is attached to a Responsibility with node id 11 in SSM with id 1196: different node, different SSM.</li>
</p>
 
<p>So the analyst would look at the first "money" node text item and see that it's associated with Responsibility r26-1234 ("...health") and would choose to place it under some code like "Child's Health Care Need."</p>

<p>The analyst would look at the second "money" text item and see that it's associated with Responsibility r23-1234 ("...education"). Although the node text is identical to that of the preceding, it's associated with a different Responsibility that would indicate a different coding, say "Child's Education Need."</p>

<p>For the third node text item the analyst would look at the associated Responsibility -- child's education r11-1196 -- and conclude that it should also be coded under "Child's Education Need," even though it's not only associated with a different Responsibility but that it's from a different SSM. However, although the actual Responsibility node is different (it's in a different SSM) it's semantically similar (in this case identical) to the Responsibility with r-label r23-1234, so it would belong under the same code. That would be the analyst's judgment call, easy here because the two Responsibilities (r23-1234 and r11-1196​) have identical text, but it may not always be so obvious.</p>

<p>Note that the RESPONSIBILITY node text items have their own "r-labels" attached so that the analyst can look them up by r-label to determine how to code all the other  associated node text items.</p>

<p>ROLE node text items wouldn't get r-labels. Neither, of course, would text from any nodes that aren't attached to any Responsibilities.</p>

<p>If a node is attached to multiple Responsibilities, it gets multiple r-labels, one for each. How does the analyst handle such an eventuality? I guess it will be a judgement call.</p>
