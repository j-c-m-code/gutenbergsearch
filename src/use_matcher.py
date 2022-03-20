"""
Loads an existing Spacy doc then uses the Matcher on it
"""
# first import standard modules
import glob
import os
from pathlib import Path

# import third-party modules
import spacy
from spacy.tokens import Doc
from spacy.matcher import Matcher

# then import my own code (PEP-8 convention)
from askdir import whichdir
import terms as tm

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
    {"LEMMA": {"IN": tm.bodypart_list}, "DEP": "dobj"},
]

matcher.add("PATTERNS", [verb_pattern, body_pattern])

directoryname = whichdir()

os.chdir(directoryname)

filelist = glob.glob("*")


def process_match(sentence):
    print(sentence)
    to_label = yes_or_no()
    if to_label:
        with open(
            rf"C:\Users\james\testing use_matcher output.txt",
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
    with open(
        rf"C:\Users\james\{short_name} use_matcher output.txt", "w", encoding="utf-8"
    ) as writer:
        writer.write("Match number " + str(COUNTER) + "\n")
        writer.write("from " + str(Path(filename)) + "\n")
        # sent is a Spacy span object.
        # ask for its text attribute to get the text
        writer.write(sent.text)
        writer.write("\n\n")


for filename in filelist:

    doc = Doc(nlp.vocab).from_disk(filename)

    sentences = list(doc.sents)

    COUNTER = 0

    short_name = Path(filename).stem

    for sent in sentences:
        # Spacy matcher works on a Doc or a Span (calling with a Span here)
        matches = matcher(sent)
        if len(matches) > 0:
            # sent.text sends only the text of the sentence,
            # not the Spacy object
            process_match(sent.text)
