"""
Loads an existing Spacy doc then uses the Matcher on it
"""
# first import standard modules
from pathlib import Path

# import third-party modules
import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
from spacy.matcher import Matcher

# then import my own code (PEP-8 convention)
from askfile import whichfile
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

matcher.add("VERB_PATTERN", [verb_pattern])


filename = whichfile()

doc = Doc(Vocab()).from_disk(filename)

sentences = list(doc.sents)

counter = 0

short_name = Path(filename).stem

with open(short_name + ".txt", "w") as writer:
    for sent in sentences:
        matches = matcher(sent)
        if len(matches) > 0:  # if we found at least one match
            counter += 1
            writer.write("Match number " + str(counter))
            writer.write("from " + filename)
            # sent is a Spacy span object.
            # ask for its text attribute to get the text
            writer.write(sent.text)) 
            writer.write()
