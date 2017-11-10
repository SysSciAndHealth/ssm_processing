<h3>add_codes_to_SSMs</h3>

<p>
add_codes_to_SSMs.py accepts three arguments: the first is the path to a
directory of  SSM JSON files (see https://github.com/steve9000gi/ssm), the
second is the path to a directory of related CBLM files (see
https://github.com/steve9000gi/AddCodesToBLM), and the third is the path to a 
directory into which the CSSMs (Coded System Support Maps) will be placed. It
reads each SSM and its associated CBLM file, finds the code associated with each
SSM node from the CBLM, adds that code to the corresponding node in the SSM as a
new key/value pair, and writes the updated JSON object to a file in the
directory specified by the third command-line argument.
</p>

<p>
Usage:<br>
./add_codes_to_SSMs.py ssm_dir cblm_dir cssm_dir<br><br>

Assumes that each SSM in ssm_dir has a corresponding CBLM file in cblm_dir,
and that the files for all three directories follow this naming convention:
<ul>
<li>SSM : "_name_.json"</li>
<li>CBLM: "_name_-CBLM.csv"</li>
<li>CSSM: "_name_-C.json"</li>
</ul>
where _name_ is a string that may or may not be constructed according to a
convention defined in
https://github.com/steve9000gi/extractMaps/blob/master/README.md.
</p>
