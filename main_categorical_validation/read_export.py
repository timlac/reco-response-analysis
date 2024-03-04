import pandas as pd
import json
from nexa_preprocessing.utils.time_series_operations import slice_by


df = pd.read_csv("../data/main_categorical_validation/full_export.csv")


count_of_rows = len(df[df['emotion_id_reply'] == 1000])
print("Number of rows where emotion_id_reply is equal to 1000:", count_of_rows)

count_of_rows = len(df[df['emotion_id_reply'] != 1000])
print("Number of rows where emotion_id_reply is NOT equal to 1000:", count_of_rows)

slices = slice_by(df, "alias")

complete_aliases = []
incomplete_aliases = []

for s in slices:
    all_rows_equal_1000 = (s['emotion_id_reply'] == 1000).all()
    if not all_rows_equal_1000:
        has_emotion_id_1000 = (s['emotion_id_reply'] == 1000).any()
        if has_emotion_id_1000:
            incomplete_aliases.append(s)
        else:
            complete_aliases.append(s)

df = pd.concat(complete_aliases, ignore_index=True)

df.to_csv("data/completed_export.csv", index=False)


complete_and_incomplete_aliases = complete_aliases + incomplete_aliases

df = pd.concat(complete_and_incomplete_aliases, ignore_index=True)
df.to_csv("data/incomplete_export.csv", index=False)





# # Specify the path to your JSON file
# meta_file_path = "data/meta.json"

# # Open and read the JSON file
# with open(meta_file_path, 'r') as json_file:
#     # Load the JSON data into a Python dictionary
#     data_dict = json.load(json_file)
#
#
# filtered_aliases = []
# for s in complete_aliases:
#     if s["alias"].isin(data_dict).any():
#         filtered_aliases.append(s)
#
#
# df = pd.concat(filtered_aliases, ignore_index=True)
# df.to_csv("data/export")

# for s in filtered_aliases:
#     # get alias
#     alias_all_unique = s["alias"].unique()
#     assert len(alias_all_unique) == 1
#     alias = alias_all_unique[0]
#
#     # get metadata
#     meta = data_dict[alias]
#
#     print(meta)
#





