import pandas as pd
import numpy as np

df = pd.read_excel("template.xlsx")

# iterate over the rows of the dataframe
for index, row in df.iterrows():
    print(row["Column1"], row["Column2"])
