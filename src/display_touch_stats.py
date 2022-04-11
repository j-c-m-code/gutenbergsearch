"""
Displays statistics for self-touch in selected novels
"""
import pandas

import askfile

print("Which CSV file for input?")
input_file = askfile.whichfile()

input_frame = pandas.read_csv(input_file, encoding="UTF-8")

# multiplying numerator by 10000 for easier reading
input_frame["self_touch"] = (
    10000 * input_frame["true_positives"] / (input_frame["word_count"])
)

input_frame.sort_values(by="self_touch", ascending=False)

input_frame.to_csv("out.csv", encoding="UTF-8")
