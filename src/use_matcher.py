"""
Loads a folder of existing Spacy docs then uses the Matcher on them
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
            rf"C:\Users\james\OneDrive\Desktop\{short_name} use_matcher output.txt",
            "a",  # we want append mode, not write mode
            encoding="utf-8",
        ) as writer:
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
    for sent in sentences:
        # Spacy matcher works on a Doc or a Span (calling with a Span here)
        matches = matcher(sent)
        if len(matches) > 0:
            # sent.text sends only the text of the sentence,
            # not the Spacy object
            process_match(sent.text)
