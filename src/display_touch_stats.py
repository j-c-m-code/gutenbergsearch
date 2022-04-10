import pandas


import askfile

print("Which CSV file for input?")
input_file = askfile.whichfile()

input_frame = pandas.read_csv(input_file, encoding="UTF-8")

print(input_frame)

input_frame["self_touch"] = input_frame["true_positives"] / (
    input_frame["false_positives"] + input_frame["all_negatives"]
)

input_frame.sort_values(by="self_touch", ascending=False)
