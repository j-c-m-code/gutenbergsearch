"""
Loads an existing Spacy doc then uses the Matcher on it
"""

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

matcher.add("BODY_PATTERN", [body_pattern])

# pattern for "he touched her arm"--verb from list then body part as object?

# write a wrapper which pulls in one of several patterns?

filename = whichfile()

doc = Doc(Vocab()).from_disk(filename)

sentences = list(doc.sents)

counter = 0

for sent in sentences:
    matches = matcher(sent)
    if len(matches) > 0:  # if we found at least one match
        counter += 1
        print("Match number " + str(counter))
        print("from " + filename)
        print(sent)
        print()
