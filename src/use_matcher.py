"""
Loads an existing Spacy doc then uses the Matcher on it
"""
import glob
import os
from pathlib import Path

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc

import terms as tm
from askdir import whichdir

nlp = spacy.load("en_core_web_lg")

matcher = Matcher(nlp.vocab)

body_pattern = [
    # a body part (noun)
    {"LEMMA": {"IN": tm.bodypart_list}, "POS": "NOUN"},
    # zero or more non-body-part tokens
    {"LEMMA": {"NOT_IN": tm.bodypart_list}, "OP": "*"},
    # a body part (noun)
    {"LEMMA": {"IN": tm.bodypart_list}, "POS": "NOUN"},
]

verb_pattern = [
    # a touch verb
    {"LEMMA": {"IN": tm.touch_list}, "POS": "VERB"},
    # zero or more non-body-part tokens
    {"LEMMA": {"NOT_IN": tm.bodypart_list}, "OP": "*"},
    # a body part that is a direct object
    # dependencies must be LOWERCASED
    {"LEMMA": {"IN": tm.bodypart_list}, "DEP": {"IN": ["dobj", "pobj"]}},
]

matcher.add("PATTERNS", [verb_pattern, body_pattern])

directoryname = whichdir()

os.chdir(directoryname)

filelist = glob.glob("*")


def process_match(sentence):
    """
    Is this a real match?
    If yes, write it to the txt file
    """
    print(sentence)
    to_label = yes_or_no()
    if to_label:
        with open(
            rf"C:\Users\james\{short_name} use_matcher output.txt",
            "w",
            encoding="utf-8",
        ) as writer:
            writer.write("from this file\n")
            # sent is a Spacy span object.
            # ask for its text attribute to get the text
            writer.write(sentence)
            writer.write("\n\n")


def yes_or_no():
    """
    asks for input; validates for 'y' or 'n'
    """
    while "the answer is invalid":
        reply = str(input("Label as touch? (y/n) > ")).lower().strip()
        if reply[:1] == "y":
            return True
        if reply[:1] == "n":
            return False


for filename in filelist:
    doc = Doc(nlp.vocab).from_disk(filename)
    sentences = list(doc.sents)
    short_name = Path(filename).stem
