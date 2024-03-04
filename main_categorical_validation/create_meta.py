import pandas as pd
from pprint import pprint
import json

path = "../data/main_categorical_validation/data vali ht23.xlsx"

df = pd.read_excel(path)

df.drop_duplicates(subset="alias", inplace=True)

data = json.loads(df.to_json(orient="records"))

out = {}
for i in data:
    out[i["alias"]] = i
    del out[i["alias"]]["alias"]


# Writing to sample.json
with open("../data/main_categorical_validation/meta.json", "w") as outfile:
    outfile.write(json.dumps(out))
