"""
Removes lines that are part of the Project Gutenberg header or footer.
"""
from gutenberg_strings import TEXT_START_MARKERS
from gutenberg_strings import TEXT_END_MARKERS


def strip_headers(text):
    """Remove lines that are part of the Project Gutenberg header or footer.
    Note: this function is a port of the C++ utility by Johannes Krugel. The
    original version of the code can be found at:
    http://www14.in.tum.de/spp1307/src/strip_headers.cpp
    Args:
        text (unicode): The body of the text to clean up.
    Returns:
        unicode: The text with any non-text content removed.
    """
    lines = text.splitlines(True)  # True option means keep line endings

    out = []

    for line in lines:
        if any(line.startswith(token) for token in TEXT_END_MARKERS):
            break
        elif any(line.startswith(token) for token in TEXT_START_MARKERS):
            out = []
        else:
            out.append(line)
    return "".join(out)
