# <codecell>
import numpy as np
import pandas as pd
import matplotlib.pyplot as pyplot

import askfile as af

# <codecell>
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_lg")

# <codecell>
file_to_read = af.whichfile()

# <codecell>
data_frame = pd.read_csv(file_to_read, nrows=35, encoding="UTF-8", usecols=["text"])
texts = [_ for _ in data_frame["text"]]

doc = nlp("What is a cat?")
displacy.render(doc)
spacy.explain("AUX")
