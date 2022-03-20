"""
Processes .txt file to Spacy doc then saves the doc
"""
# first import standard modules
from pathlib import Path

# then import third-party modules
import spacy

# finally import my own code (PEP-8 convention)
from askfile import whichfile

nlp = spacy.load("en_core_web_lg")

filename = whichfile()
short_name = Path(filename).stem

with open(filename, "r", encoding="utf-8") as f:
    novel = f.read()

# the novel is too long for the default, so increase allocated memory
nlp.max_length = len(novel) + 100

# Process a text
doc = nlp(novel)

# r for raw string--no escape characters
# f for format string--allow me to pass in variable
doc.to_disk(rf"C:\Users\james\{short_name}")
