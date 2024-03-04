import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
from nexa_preprocessing.utils.time_series_operations import slice_by


def map_sex(sex):
    if sex == "m":
        return "male"
    elif sex == "k":
        return "female"
    elif pd.isna(sex):
        return "unknown"
    else:
        raise ValueError("Something went wrong, sex is: {}".format(sex))


def map_reply(reply):
    # Check if a string (representing an integer) is within the range [0, 44]
    try:
        value_int = int(reply)
        if 0 <= value_int <= 43:
            return str(value_int)
        else:
            return ""
    except ValueError:
        print(f"{reply} is not a valid integer")


column_map = {
    "ID": "user_id",
    "alias": "survey_id",
    "födelseår": "date_of_birth",
    "processed_status": "has_reply",
    "emotion_id_reply": "reply",
    "emotion_options": "emotion_alternatives"}

meta_columns = ["user_id", "survey_id", "valence", "sex", "date_of_birth", "emotion_alternatives"]

item_columns = ["filename", "emotion_id", "video_id", "reply", "has_reply"]


df = pd.read_csv("../data/main_categorical_validation/incomplete_export.csv", converters={"emotion_options": pd.eval})


# Specify the path to your JSON file
meta_file_path = "../data/main_categorical_validation/meta.json"

# Open and read the JSON file
with open(meta_file_path, 'r') as json_file:
    # Load the JSON data into a Python dictionary
    data_dict = json.load(json_file)

for index, row in df.iterrows():
    alias = row['alias']
    if alias in data_dict:
        json_entry = data_dict[alias]
        for key, value in json_entry.items():
            df.at[index, key] = value

df.rename(columns=column_map, inplace=True)

# Add ".mp4" to all filenames in the 'filename' column
df['filename'] = df['filename'].apply(lambda x: x + '.mp4')

df["sex"] = df["sex"].apply(map_sex)
df["reply"] = df["reply"].apply(map_reply)

df["date_of_birth"] = df["date_of_birth"].astype("Int64")

slices = slice_by(df, "survey_id")


def get_array_val(arr):
    if pd.isna(arr).any():
        print("NaN in array, returning None")
        return None
    # assert that we have only extracted one identifier per dataframe
    if len(np.unique(arr)) != 1:
        raise ValueError("something went wrong, more than one {} found for time series".format(arr))
    else:
        return arr[0]


ret = []
for df_slice in slices:
    survey = {}
    for column in meta_columns:

        val = get_array_val(df_slice[column].values)
        if column == "user_id" and not val:
            val = uuid.uuid4().hex

        if column == "date_of_birth" and val:
            val = int(val)

        survey[column] = val

    survey_items = []
    for index, row in df_slice.iterrows():
        survey_items.append(row[item_columns].to_dict())

    survey["survey_items"] = survey_items

    ret.append(survey)

with open('../surveys.json', 'w') as f:
    json.dump(ret, f)

