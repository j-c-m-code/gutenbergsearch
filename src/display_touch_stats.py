import csv
import os
import pandas

import seaborn
import spacy

import askfile

print("Which CSV file for input?")
input_file = askfile.whichfile()

input_frame = pandas.read_csv(input_file, encoding="UTF-8")
