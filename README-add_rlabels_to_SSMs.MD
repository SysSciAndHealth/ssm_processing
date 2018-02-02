<h1>README: add_rlabels_to_SSMs.py</h1>

<p>An <em>rlabel</em> is a string that uniquely identifies a Responsibility node in the context of a set (a directory) of System Support Maps (SSMs).</p>

<p>
    Usage:
        add_rlabels_to_SSMs.py indir outdir [use_full_filename] [undir]

    Args:
        indir: String path to a directory of System Support Map (SSM) files.
            Expects the files to be in JSON format and end with extension
            ".json."
        outdir: String path to a directory that is the intended target location
            for a set of rlinked ssm files. If outdir doesn't exist, a
            reasonable attempt will be made to create it.
        use_full_filename (optional): Boolean. If true, create rlabel using
            the whole input SSM filename (excepting the ".json" extension).
            False is the default, in which case the SSM filename is expected to
            have the form "text<database id>.json, where <database id is the
            SSM's id in the server PostgreSQL database.
        undir (optional): Boolean. if True, use an undirected graph traversal.
            Otherwise, consider edge directionality when traversing
            Responsibility subgraphs. Default is False (directed).
</p>

<h3>Naming rlabels for sets of SSMs with database ids in filenames</h3>

<p>For an SSM file with the database id as part of the filename (typically a file extracted from the server database using one of the scripts written for the purpose, e.g., https://github.com/steve9000gi/ssm_processing/blob/master/get_maps.py) the rlabel is of the form</p>

    [r<responsibility id>-<SSM id>]

<p>where</p>

    <responsibility id>

<p>is the id of a particular Responsibility node in the SSM json file whose database id is</p>

    <SSM id>.

<p>For a representative SSM named _Oneida_ffffft_bpellegr_1000.json we would assign the rlabel "[r1-1000]" to the Responsibility node with node id 1 (the SSM file was pulled from the database and it has id 1000), "[r2-1000]" to the Responsibility node with node id 2 from that same file, etc. We would then like to assign that same rlabel to any other node that's connected, directly or indirectly, to the corresponding Responsibility.</p>

<h3>Naming rlabels for sets of SSMs without database ids</h3>
<p>Some SSM sets may not be in the database -- they may have been built not with a wizard but with the basic <em>ssm</em> online tool and may have been saved only to a local machine -- and don't have database numbers. For these we use the full file name along with the Responsibility's node id, which is still unique within that file. For example, the Responsibility node with node id 2 in a file named "06.08.15_7_Fv5.json" would be assigned the rlabel "[r2-06.08.15_7_Fv5]" (we can at least lop off the standard ".json" extension from the SSM filename.) This may be more cumbersome than is ideal, but it maximizes the probability that we uniquely identify a specific Responsibility within a set of SSMs when SSM database ids are unavailable.</p>

<p>With this tool we offer two ways to determine connectivity. Each has its virtues and shortcomings.</p>

<h3>Undirected graph traversal</h3>
<p>Treating an SSM as an undirected graph allows us to track even the most indirect connections between a Responsibility and other nodes. This allows us to rlabel nodes that are only indirectly connected to a given Responsibility, notably Wishes and Resources, even though the edges point inward toward their Responsibilities.</p>

<p>However, there are shortcomings to the undirected approach. Often, particularly with wizard-built maps, there are enough links (i.e., edges or arrows) and they are sufficiently intertwined that, when the Responsibility node subgraphs for this map are traversed using an undirected algorithm, we find that almost every node is eventually connected to every Responsibility node -- you can trace the connections manually by ignoring edge direction -- and as a consequence most of the non-Responsibility nodes (ignoring the Role, which is excluded in code) exhibit all of the rlabels, thus rendering the rlabeling process useless for this very common SSM node configuration. The algorithm appears to work "correctly"; unfortunately, it doesn't appear to do us much good in this case.</p>

<h3>Directed graph traversal</h3>
<p>With this approach we consider the directionality of the links between the nodes. This approach would probably work very well if all the links pointed outward. Unfortunately, the convention has been established that links from Resources and Wishes point inwards. The directed traversal implementation accurately identifies what Needs are connected to which Responsibility. However, we can't find which Resources and Wishes may be connected indirectly to a certain Responsibility through an intermediary node, typically a Need, because the arrows change direction.</p>

</p>Need node text here includes rlabels that correctly identify the Responsibility nodes they are attached to. On the plus side, there isn't the obfuscating clutter of extraneous rlabels we see in the undirected traversal implementation. However, the inward-pointing Resource and Wish nodes are not rlabeled, so we are unable to use rlabeling to distinguish between them.

<h3>Recommendation</h3>
<p>For the future, I believe that pointing all arrows in a consistent direction would make the directed rlabeling process work well. There's still the legacy of existing sets of maps, however. Rather more intimidating is the prospect of changing half a dozen wizards to suit such a new convention.</p>

</p>A directed implementation currently offers a limited but useful disambiguating capability, although Resources and Wishes are excluded.</p>

<h3>Example</h3>
<p>From some aggregated.txt (or NEEDS.txt), ie., a file of node text items to be sorted under various <em>codes</em> (see https://github.com/steve9000gi/sort for details of the coding process). There are these two (originally identical) node text items in the NEEDS list:

    ...
    time commitment [r4-1000]
    time commitment [r5-1000]
    ...

Without the appended rlabels these two items would be indistinguishable and would probably both be coded the same. However, we see from the rlabels that the first is connected to the Responsibility with id = 4  and the second to the Responsibility with id = 5 from the SSM with database id 1000. The sorting analyst can look under RESPONSIBILITIES and find the corresponding node texts: 

    ...
    County Fiscal Team for Special Children's Services division [r4-1000]
    Early Intervention Coordinating Council participant [r5-1000]
    ...

Those could very well require different codes, and the analyst now has this additional information (via rlabel) to better inform her decision: whether to assign each the same or a different code. These two identical Responsibility nodes happen to be from the same SSM, but this whole process should apply just as well if they come from different maps. We've seen this replication frequently with Needs like "time" or "money."</p>

<h3>Another example</h3>
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

and without additional information the analyst would now conclude that all three "money" node text items belong under a single code, say "Money Needs".</p>

<p>Rlabeling would provide this information:

    ...
    RESPONSIBILITIES:
    ...
    child's health [r26-1234]
    child's education [r23-1234]
    child's education [r11-1196]
    ...
    NEEDS:
    ...
    money [r26-1234]
    money [r23-1234]
    money [r11-1196]
    ...

</p>

<p>This would mean that:

<ul>
<li>The first "money" node text item is attached to a Responsibility with node id 26 in the SSM with id 1234.</li>
<li>The second "money" node text item is attached to a Responsibility with node id 23 in the SSM with id 1234. It's in the same SSM but attached to a different Responsibility and thus might or might not be coded differently, depending on the text for the Responsibility node[s] involved.</li>
<li>The third "money" node text item is attached to a Responsibility with node id 11 in SSM with id 1196: different node, different SSM.</li>
</ul>
</p>
 
<p>So the analyst would look at the first "money" node text item and see that it's associated with Responsibility [r26-1234] ("...health") and would choose to place it under some code like "Child's Health Care Need."</p>

<p>The analyst would look at the second "money" text item and see that it's associated with Responsibility [r23-1234] ("...education"). Although the node text is identical to that of the preceding, it's associated with a different Responsibility that would indicate a different coding, say "Child's Education Need."</p>

<p>For the third node text item the analyst would look at the associated Responsibility &mdash; child's education [r11-1196] &mdash; and conclude that it should also be coded under "Child's Education Need," even though it's not only associated with a different Responsibility <em>and</em> it's from a different SSM. However, although the actual Responsibility node is different (it's in a different SSM) it's semantically similar (in this case identical) to the Responsibility with rlabel [r23-1234], so it would belong under the same code. That would be the analyst's judgment call, easy here because the two Responsibilities ([r23-1234] and [r11-1196]) have identical text, but it may not always be so obvious.</p>

<p>Note that the RESPONSIBILITY node text items have their own rlabels attached so that the analyst can look them up by rlabel to determine how to code all the other  associated node text items.</p>

<p>ROLE node text items wouldn't get rlabels. Neither, of course, would text from any nodes that aren't attached to any Responsibilities.</p>

<p>If a node is attached to multiple Responsibilities, it gets multiple rlabels, one for each. How does the analyst handle such an eventuality?</p>

