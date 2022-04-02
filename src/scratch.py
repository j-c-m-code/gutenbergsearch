# <codecell>
import csv
import os
import pandas

import matplotlib.pyplot
import seaborn
import spacy

import askdir
import askfile
import use_matcher

# <codecell>
nlp = spacy.load("en_core_web_lg")
matcher = spacy.matcher.Matcher(nlp.vocab)

# <codecell>
input_file = askfile.whichfile()

# <codecell>
input_frame = pandas.read_csv(input_file, encoding="UTF-8")

sentences = [_ for _ in input_frame["sentence"]]
self_touch_actuals = [_ for _ in input_frame["self_touch_actual"]]


# <codecell>
matcher.add(
    "PATTERNS", [use_matcher.subject_pattern, use_matcher.object_pattern]
)  # type: ignore

output_directory = askdir.whichdir()

os.chdir(output_directory)

with open("test_output.csv", "a", newline="", encoding="UTF-8") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "self_touch_actual", "self_touch_predicted"])
    for count, sentence in enumerate(sentences):
        doc = nlp(sentence)
        matches = matcher(doc)
        if len(matches) > 0:
            writer.writerow([sentence, self_touch_actuals[count], "yes"])
        else:
            writer.writerow([sentence, self_touch_actuals[count], "no"])

# <codecell>
output_file = askfile.whichfile()
output_frame = pandas.read_csv(output_file, encoding="UTF-8")
# mapping "yes" to 1 and "no" to 0 for display
# output_frame["self_touch_actual"] = output_frame["self_touch_actual"].map(
#     {"yes": 1, "no": 0}
# )
# output_frame["self_touch_predicted"] = output_frame["self_touch_predicted"].map(
#     {"yes": 1, "no": 0}
# )
confusion_matrix = pandas.crosstab(
    output_frame["self_touch_actual"],
    output_frame["self_touch_predicted"],
    rownames=["Actual"],
    colnames=["Predicted"],
)

# group_names = ["True Neg", "False Pos", "False Neg", "True Pos"]

seaborn.heatmap(confusion_matrix, annot=True, cmap="Blues")
matplotlib.pyplot.show()
