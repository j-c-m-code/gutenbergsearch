"""testing out the matcher"""
# <codecell>
import csv
import os
import matplotlib.pyplot
import pandas


import seaborn
import spacy

import askdir
import askfile
import patterns

# <codecell>
nlp = spacy.load("en_core_web_lg", disable=["ner"])
matcher = spacy.matcher.Matcher(nlp.vocab)

# <codecell>
print("Which CSV file for input?")
input_file = askfile.whichfile()

# <codecell>
input_frame = pandas.read_csv(input_file, encoding="UTF-8")

sentences = list(input_frame["sentence"])
self_touch_actuals = list(input_frame["self_touch_actual"])


# <codecell>
matcher.add(
    "PATTERNS",
    [patterns.subject_pattern, patterns.object_pattern, patterns.body_pattern],
)  # type: ignore

print("Which dirctory for output?")
output_directory = askdir.whichdir()

os.chdir(output_directory)

"""
Unless I use Windows-1252 encoding instead of UTF-8, some characters like
LATIN SMALL LETTER E WITH ACUTE come out garbled
"""

with open("test_output.csv", "w", newline="", encoding="Windows-1252") as file:
    writer = csv.writer(file, dialect="excel")
    writer.writerow(["text", "self_touch_actual", "self_touch_predicted"])
    for count, sentence in enumerate(sentences):
        doc = nlp(sentence)
        matches = matcher(doc)
        if len(matches) > 0:
            # print(sentence)
            writer.writerow([sentence, self_touch_actuals[count], "yes"])
        else:
            writer.writerow([sentence, self_touch_actuals[count], "no"])

# <codecell>
print("Which CSV file to create confusion matrix?")
matrix_input_file = askfile.whichfile()
# have to use Windows-1252 because it's what I used above
output_frame = pandas.read_csv(matrix_input_file, encoding="Windows-1252")

confusion_matrix = pandas.crosstab(
    output_frame["self_touch_actual"],
    output_frame["self_touch_predicted"],
    rownames=["Actual"],
    colnames=["Predicted"],
)

heat_map = seaborn.heatmap(confusion_matrix, annot=True, cmap="Blues")

# saves a png of the heatmap we just created
matplotlib.pyplot.savefig("test on labeled sentences.png")
