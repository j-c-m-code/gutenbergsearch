# <codecell>
import numpy as np
import pandas as pd
import matplotlib.pyplot as pyplot

import askfile as af

# <codecell>
file_to_read = af.whichfile()

# <codecell>
data_frame = pd.read_csv(file_to_read, nrows=35, encoding="UTF-8", usecols=["text"])
texts = [_ for _ in data_frame["text"]]
