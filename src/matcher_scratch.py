# import third-party modules
import spacy
from spacy.matcher import Matcher

# then import my own code (PEP-8 convention)
import terms as tm

TEST_TEXT = """
His eyes roamed her face and her eyes. I touch your ear.

"""


def on_match(matcher, doc, id, matches):
    print(id)
    print(sent)
    to_label = yes_or_no()
    print(to_label)


def yes_or_no():
    while "the answer is invalid":
        reply = str(input("Label as touch? (y/n) > ")).lower().strip()
        if reply[:1] == "y":
            return True
        if reply[:1] == "n":
            return False


nlp = spacy.load("en_core_web_lg")

matcher = Matcher(nlp.vocab)

doc = nlp(TEST_TEXT)

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

matcher.add("PATTERNS", [verb_pattern, body_pattern], on_match=on_match)

sentences = list(doc.sents)

for sent in sentences:
    # Spacy matcher works on a Doc or a Span (calling with a Span here)
    matches = matcher(sent, as_spans=True)
#    breakpoint()
