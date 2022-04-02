# <codecell>
import csv
import os
import pandas

import spacy

import askdir
import askfile
import use_matcher

# <codecell>
nlp = spacy.load("en_core_web_lg")
matcher = spacy.matcher.Matcher(nlp.vocab)

# <codecell>
file_to_read = askfile.whichfile()

# <codecell>
data_frame = pandas.read_csv(file_to_read, encoding="UTF-8")

texts = [_ for _ in data_frame["text"]]
labels = [_ for _ in data_frame["label"]]


# <codecell>
matcher.add(
    "PATTERNS", [use_matcher.subject_pattern, use_matcher.object_pattern]
)  # type: ignore

output_directory = askdir.whichdir()

os.chdir(output_directory)

with open("test_output.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "label", "result"])
    for count, text in enumerate(texts):
        doc = nlp(text)
        matches = matcher(doc)
        if len(matches) > 0:
            writer.writerow([text, labels[count], "Positive"])
        else:
            writer.writerow([text, labels[count], "Negative"])
