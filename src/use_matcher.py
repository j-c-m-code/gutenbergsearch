"""
Loads a folder of existing Spacy docs then uses the Matcher on them
"""
import glob
import os
from pathlib import Path

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc

import patterns
from askdir import whichdir

# not using named entity recognition, so disable it for speed
nlp = spacy.load("en_core_web_lg", disable=["ner"])
matcher = Matcher(nlp.vocab)

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


def write_results(
    sentence_list: list, match_list: list, short_nm: str, output_dir: str
) -> None:
    """
    Writes all the matched sentences to a txt file
    along with some surrounding sentences for context
    """
    context_distance = 2

    with open(
        rf"{output_dir}\{short_nm} use_matcher output.txt",
        "a",  # we want append mode, not write mode
        encoding="utf-8",
    ) as writer:
        # match is a list of indices
        for match in match_list:
            writer.write("Match in sentence " + str(match) + " from " + short_nm + "\n")
            # prints context around the match
            # remember, range stops BEFORE the stop argument
            for i in range(0, 2 * context_distance + 1):
                index = match - context_distance + i
                text_to_write = sentence_list[index].text
                writer.write(text_to_write)
                # puts a space after each sentence but the last
                if i < 2 * context_distance:
                    writer.write(" ")
            writer.write("\n\n\n")


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
    matcher.add(
        "PATTERNS",
        [patterns.subject_pattern, patterns.object_pattern, patterns.body_pattern],
    )  # type: ignore
    source_directory = whichdir()
    os.chdir(source_directory)
    filelist = glob.glob("*")
    # output_directory = whichdir()

    test_counter = 0

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
                test_counter += 1
                # sent.text sends only the text of the sentence,
                # not the Spacy object
                if is_match(sent.text):
                    matchlist.append(count)
        print("We got " + str(test_counter) + " total matches")
        print("There were " + str(len(matchlist)) + " true positives")
        print("There were " + str(test_counter - len(matchlist)) + " false positives")
        print((str(len(sentences) - test_counter)) + " were not matched")
        # write_results(sentences, matchlist, short_name, output_directory)
