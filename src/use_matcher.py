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


# using type hints
def is_match(sentence: str) -> bool:
    """
    Is this a real match?
    Return True or False
    """
    print(sentence)
    to_label = yes_or_no()
    # below line returns either True or False
    # Pylint prefers this structure over an if ... else
    return bool(to_label)


def write_results(sentence_list: list, match_list: list, short_nm: str) -> None:
    """
    Writes all the matched sentences to a txt file
    along with some surrounding sentences for context
    """
    CONTEXT_DISTANCE = 1
    output_directory = whichdir()

    with open(
        rf"{output_directory}\{short_nm} use_matcher output.txt",
        "a",  # we want append mode, not write mode
        encoding="utf-8",
    ) as writer:
        # match is a list of indices
        for match in match_list:
            writer.write("Match in sentence " + str(match) + " from " + short_nm + "\n")
            # prints from one sentence before to one
            # sentence after the match
            text_to_write = sentence_list[match - CONTEXT_DISTANCE].text
            writer.write(text_to_write)
            writer.write("\n\n")


def yes_or_no() -> bool:
    """
    asks for input; validates for 'y' or 'n'
    """
    # this loop works because non-empty strings evaluate as truthy in Python
    while "the answer is invalid":
        reply = str(input("Label as touch? (y/n) > ")).lower().strip()
        if reply[:1] == "y":
            return True
        if reply[:1] == "n":
            return False


if __name__ == "__main__":

    matcher.add("PATTERNS", [verb_pattern, body_pattern])  # type: ignore
    source_directory = whichdir()
    os.chdir(source_directory)
    filelist = glob.glob("*")

    for filename in filelist:
        matchlist = []
        doc = Doc(nlp.vocab).from_disk(filename)
        # a sent is a kind of Span
        sentences = list(doc.sents)
        short_name = Path(filename).stem
        for count, sent in enumerate(sentences):
            # Spacy matcher works on a Doc or a Span (calling with a Span here)
            matches = matcher(sent)
            if len(matches) > 0:
                # sent.text sends only the text of the sentence,
                # not the Spacy object
                if is_match(sent.text):
                    matchlist.append(count)
        write_results(sentences, matchlist, short_name)
