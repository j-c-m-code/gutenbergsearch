"""
Intended to clean up and overwrite
utf-8 text files downloaded from
Project Gutenberg

expects Windows line endings: \r\n
"""
# first import standard modules
import re

# then third-party modules
from fs.osfs import OSFS

# then my modules
import askdir as ad
import clean_gutenberg_headers as cgh

DIRECTORY = ad.whichdir()


def _main():

    with OSFS(DIRECTORY) as myfs:
        for path in myfs.walk.files(filter=["*.txt"]):
            # print(path)
            with myfs.open(
                path
            ) as current_file:  # defaults to read mode and utf-8 encoding
                # reading original file
                contents = current_file.read()
                # stripping the headers
                contents = cgh.strip_headers(contents)

                # removes chapter numbers;
                # finds lines with only "Chapter III" or "III" on them
                # Python expects \n, not \r\n, so I can't use start/end anchors
                # and the Multiline flag doesn't help me
                chapter_line_roman = re.compile(
                    r"""
                    (\r\n)               # start of line
                    (chapter|book|part)? # optional at start of the line
                    (\ )?                # optional space
                    [MDCLXVI]+           # roman numerals
                    (\r\n)               # end of line
                    """,
                    flags=re.IGNORECASE | re.VERBOSE,
                )

                contents = re.sub(chapter_line_roman, "\r\n", contents)

                chapter_line_numeric = re.compile(
                    r"""
                    (\r\n)               # start of line
                    (chapter|book|part)? # optional at start of the line
                    (\ )?                # an optional space
                    [\d]+                # digits
                    (\r\n)               # end of line
                    """,
                    flags=re.IGNORECASE | re.VERBOSE,
                )

                contents = re.sub(chapter_line_numeric, "\r\n", contents)

                # project gutenberg texts end each line with a newline;
                # code below formats for word wrap
                one_newline_from_multiple = re.compile(
                    r"""
                (?<!\r\n)   # not preceeded by newline (negative lookbehind)
                \r\n        # newline
                (?!\r\n)    # not PROceeded by newline (negative lookahead)
                """,
                    flags=re.VERBOSE,
                )

                erase_asterisk_lines = re.compile(
                    r"""
                (?<=\r\n)   # match only if preceeded by a newline (lookbehind)
                [* -]+      # match one or more asterisks/spaces/dashes
                (?=\r\n)    # match only if PROceeded by a newline (lookahead)
                """,
                    flags=re.VERBOSE,
                )

                contents = re.sub(one_newline_from_multiple, r" ", contents)

                contents = re.sub(erase_asterisk_lines, r"", contents)

                # replace one or more newlines with one newline
                contents = re.sub(r"(\r\n)+", r"\1", contents)

                # replace one or more spaces with one space
                contents = re.sub(r"( )+", r"\1", contents)

                # replace underscores (sometimes used to indicate italics)
                # with nothing
                contents = re.sub(r"_", "", contents)

                # replace left/right single quote marks with apostrophe
                # (which is also the ASCII "regular" single quote mark)
                contents = re.sub(r"[‘’]", r"'", contents)

                # replace two hyphens with an em dash
                contents = re.sub(r"--", r"—", contents)

                # replace left/right quote marks with standard quote mark
                # note I use single quotes to specify the strings here b/c
                # otherwsie my replacement quotation mark gets messed up
                contents = re.sub(r"[“”]", r'"', contents)

            with myfs.open(path, mode="w") as current_file:
                # overwriting original file with the stripped version
                current_file.write(contents)


if __name__ == "__main__":
    _main()
