"""
patterns for the Spacy Matcher
"""
import terms as tm

body_pattern = [
    # a body part (noun)
    {"LEMMA": {"IN": tm.bodypart_list}, "POS": "NOUN"},
    # zero or more non-body-part tokens
    {"LEMMA": {"NOT_IN": tm.bodypart_list}, "OP": "*"},
    # a body part (noun)
    {"LEMMA": {"IN": tm.bodypart_list}, "POS": "NOUN"},
]

object_pattern = [
    # a touch verb
    {"LEMMA": {"IN": tm.touch_list}, "POS": "VERB"},
    # zero or more non-body-part tokens
    {"LEMMA": {"NOT_IN": tm.bodypart_list}, "OP": "*"},
    # a body part that is an object
    # dependencies must be LOWERCASED
    {"LEMMA": {"IN": tm.bodypart_list}, "DEP": {"IN": ["dobj", "pobj"]}},
]

subject_pattern = [
    # a body part as subject
    {"LEMMA": {"IN": tm.bodypart_list}, "DEP": {"IN": ["nsubj", "nsubjpass"]}},
    # zero or more non-body-part tokens
    {"LEMMA": {"NOT_IN": tm.bodypart_list}, "OP": "*"},
    # a touch verb
    {"LEMMA": {"IN": tm.touch_list}, "POS": "VERB"},
]

combo_pattern = [
    # a body part as subject
    {"LEMMA": {"IN": tm.bodypart_list}, "DEP": {"IN": ["nsubj", "nsubjpass"]}},
    # zero or more non-body-part tokens
    {"LEMMA": {"NOT_IN": tm.bodypart_list}, "OP": "*"},
    # a touch verb
    {"LEMMA": {"IN": tm.touch_list}, "POS": "VERB"},
    # zero or more non-body-part tokens
    {"LEMMA": {"NOT_IN": tm.bodypart_list}, "OP": "*"},
    # a body part that is an object
    # dependencies must be LOWERCASED
    {"LEMMA": {"IN": tm.bodypart_list}, "DEP": {"IN": ["dobj", "pobj"]}},
]
