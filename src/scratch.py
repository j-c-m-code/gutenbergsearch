# <codecell>
import numpy
import pandas
import matplotlib.pyplot

import spacy

import askfile
import use_matcher

# <codecell>
nlp = spacy.load("en_core_web_lg")
matcher = spacy.matcher.Matcher(nlp.vocab)

# <codecell>
file_to_read = askfile.whichfile()

# <codecell>
data_frame = pandas.read_csv(file_to_read, nrows=35, encoding="UTF-8", usecols=["text"])
texts = [_ for _ in data_frame["text"]]

# <codecell>
matcher.add("PATTERNS", [use_matcher.subject_pattern, use_matcher.object_pattern])  # type: ignore
for text in texts:
    doc = nlp(text)
    matches = matcher(doc)
    if len(matches) > 0:
        print("TRUE " + doc.text + "\n")
    else:
        print("FALSE " + doc.text + "\n")
