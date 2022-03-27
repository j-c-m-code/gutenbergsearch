"""
Processes .txt file to Spacy doc then saves the doc
"""
# first import standard modules
from pathlib import Path

# then import third-party modules
import spacy

# finally import my own code (PEP-8 convention)
from askdir import whichdir
from askfile import whichfile

nlp = spacy.load("en_core_web_lg")

source_file = whichfile()
short_name = Path(source_file).stem
output_directory = whichdir()

with open(source_file, "r", encoding="utf-8") as f:
    novel = f.read()

# the novel is too long for the default, so increase allocated memory
nlp.max_length = len(novel) + 100

# Process a text
doc = nlp(novel)

# r for raw string--no escape characters
# f for format string--allow me to pass in variable
doc.to_disk(rf"{output_directory}\{short_name}")
