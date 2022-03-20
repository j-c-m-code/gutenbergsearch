"""
Processes a folder of .txt files to Spacy docs then saves the docs
"""
# first import standard modules
import glob
import os
from pathlib import Path

# then import third-party modules
import spacy

# finally import my own code (PEP-8 convention)
from askdir import whichdir

nlp = spacy.load("en_core_web_lg")

directoryname = whichdir()
os.chdir(directoryname)
filelist = glob.glob("*")

for filename in filelist:
    with open(filename, "r", encoding="utf-8") as f:
        novel = f.read()

    # the novel is too long for the default, so increase allocated memory
    nlp.max_length = len(novel) + 100

    # Process a text
    doc = nlp(novel)

    short_name = Path(filename).stem

    # r for raw string--no escape characters
    # f for format string--allow me to pass in variable
    doc.to_disk(rf"C:\Users\james\OneDrive\Desktop\{short_name}")
