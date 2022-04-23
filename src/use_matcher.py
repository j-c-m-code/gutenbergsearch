"""
Loads an existing Spacy doc then uses the Matcher on it

This works sentence by sentence, so it will never detect self-touch
in this sentence from Custom of the Country:
'Then he felt again, more deliberately, for the spot he wanted,
and put the muzzle of his revolver against it.'
We only know "it" means his head from the PREVIOUS sentence.
"""
import csv
from datetime import datetime
from pathlib import Path

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc

import askdir
import askfile
import patterns

# not using named entity recognition, so disable it for speed
nlp = spacy.load("en_core_web_lg", disable=["ner"])
matcher = Matcher(nlp.vocab)


# using type hints
def is_match(sentence_count: int, sentence: str) -> bool:
    """
    Is this a real match?
    Return True or False
    """
    print("Sentence " + str(sentence_count) + ":")
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

    output_path = Path(rf"{output_dir}\{short_nm} use_matcher output.txt")

    # check if an output document already exists
    # if so, delete it
    if output_path.is_file():
        output_path.unlink()

    with open(
        output_path,
        "a",  # we want append mode, not write mode
        encoding="utf-8",
    ) as wrtr:
        # match is a list of indices
        for match in match_list:
            wrtr.write(
                "\nMatch in sentence " + str(match) + " from " + short_nm + "\n\n"
            )
            # prints context around the match
            # remember, range stops BEFORE the stop argument
            for i in range(0, 2 * context_distance + 1):
                index = match - context_distance + i
                if index == match:
                    text_to_write = str.upper(sentence_list[index].text)
                else:
                    text_to_write = sentence_list[index].text
                wrtr.write(text_to_write)
                # puts a space after each sentence but the last
                if i < 2 * context_distance:
                    wrtr.write(" ")
            wrtr.write("\n\n")


def yes_or_no() -> bool:
    """
    asks for input; validates for 'y' or 'n'
    """
    # this loop works because non-empty strings evaluate as truthy in Python
    while "the answer is invalid":
        reply = str(input("Label as self-touch? (y/n) > ")).lower().strip()
        if reply[:1] == "y":
            return True
        if reply[:1] == "n":
            return False


if __name__ == "__main__":
    matcher.add(
        "PATTERNS",
        [patterns.subject_pattern, patterns.object_pattern, patterns.body_pattern],
    )  # type: ignore
    print("Choose spaCy doc to work from")
    spacy_source_doc = askfile.whichfile()
    print("Choose output directory")
    output_directory = askdir.whichdir()
    time_of_run = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    test_counter = 0  # pylint: disable=invalid-name

    matchlist = []
    doc = Doc(nlp.vocab).from_disk(spacy_source_doc)
    word_count = []
    for token in doc:
        if not token.is_punct | token.is_space:
            word_count.append(token)
    # a sent is a kind of Span
    sentences = list(doc.sents)
    short_name = Path(spacy_source_doc).stem
    for count, sent in enumerate(sentences):
        # Spacy matcher works on a Doc or a Span (calling with a Span here)
        matches = matcher(sent)
        if len(matches) > 0:
            test_counter += 1
            # sent.text sends only the text of the sentence,
            # not the Spacy object
            if is_match(count, sent.text):
                matchlist.append(count)

    use_matcher_stats_path = Path(rf"{output_directory}\use_matcher stats.csv")
    # if file doesn't exist yet
    if not use_matcher_stats_path.is_file():
        with open(
            use_matcher_stats_path,
            "w",  # we want write mode here
            encoding="utf-8",
            newline="",
        ) as csvfile:
            results_file = csv.writer(csvfile, dialect="excel")
            results_file.writerow(
                [
                    "Book",
                    "Time use_matcher was run",
                    "Total sentence matches",
                    "True positives",
                    "False positives",
                    "Sentences not matched",
                    "Word count",
                ]
            )
            results_file.writerow(
                [
                    short_name,
                    time_of_run,
                    test_counter,
                    str(len(matchlist)),
                    str(test_counter - len(matchlist)),
                    str(len(sentences) - test_counter),
                    str(len(word_count)),
                ]
            )
    # if file does already exist, just append to it
    else:
        with open(
            use_matcher_stats_path,
            "a",  # we want append mode, not write mode
            encoding="utf-8",
            newline="",
        ) as csvfile:
            results_file = csv.writer(csvfile, dialect="excel")
            results_file.writerow(
                [
                    short_name,
                    time_of_run,
                    test_counter,
                    str(len(matchlist)),
                    str(test_counter - len(matchlist)),
                    str(len(sentences) - test_counter),
                    str(len(word_count)),
                ]
            )

    write_results(sentences, matchlist, short_name, output_directory)
