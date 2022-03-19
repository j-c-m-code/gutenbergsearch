# first import standard modules
import os
from pathlib import Path

# import third-party modules
import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
from spacy.matcher import Matcher

# then import my own code (PEP-8 convention)
import terms as tm

TEST_TEXT = """
This house is bigger than it looks, for it slides for two storeys down the hill behind, and the wooden door, which is always locked, really leads into the attic. The knowing person prefers to follow the precipitous mule-track round the turn of the mud wall till he can take the edifice in the rear. Then--being now on a level with the cellars--he lifts up his head and shouts. If his voice sounds like something light--a letter, for example, or some vegetables, or a bunch of flowers--a basket is let out of the first-floor windows by a string, into which he puts his burdens and departs. But if he sounds like something heavy, such as a log of wood, or a piece of meat, or a visitor, he is interrogated, and then bidden or forbidden to ascend. The ground floor and the upper floor of that battered house are alike deserted, and the inmates keep the central portion, just as in a dying body all life retires to the heart. There is a door at the top of the first flight of stairs, and if the visitor is admitted he will find a welcome which is not necessarily cold. He touched her face softly, then her eyes. There are several rooms, some dark and mostly stuffy--a reception-room adorned with horsehair chairs, wool-work stools, and a stove that is never lit--German bad taste without German domesticity broods over that room; also a living-room, which insensibly glides into a bedroom when the refining influence of hospitality is absent, and real bedrooms; and last, but not least, the loggia, where you can live day and night if you feel inclined, drinking vermouth and smoking cigarettes, with leagues of olive-trees and vineyards and blue-green hills to watch you.

"""

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

matcher.add("VERB_PATTERN", [verb_pattern])

matcher.add("BODY_PATTERN", [body_pattern])

sentences = list(doc.sents)

for sent in sentences:
    print(sent)
    print()
