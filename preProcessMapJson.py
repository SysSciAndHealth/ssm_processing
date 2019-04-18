#!/home/anaconda/anaconda2/bin/python
# Most of this was taken from 
# https://stackoverflow.com/questions/4427542/how-to-do-sed-like-text-replace-with-python
import re, shutil, tempfile, sys

def sed_inplace(filename, pattern, repl):
    '''
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    '''
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                newLine = pattern_compiled.sub(repl, line)
                tmp_file.write(newLine)
                if (line != newLine):
                  print ("Original line %s replaced with %s" % (line, newLine))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)

def main():
 
  # This pattern replaces things like [in] with '`in`'
  squareBracketFindPattern = "(.*)(\[)([a-zA-Z_0-9]*)(\])(.*)"
  squareBracketReplacePattern = "\\1'`\\3`'\\5"

  sed_inplace(sys.argv[1], squareBracketFindPattern, squareBracketReplacePattern)

if __name__== "__main__":
   main()
