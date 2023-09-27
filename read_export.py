import matplotlib
import pandas as pd
import json
import seaborn as sns

from matplotlib import pyplot as plt
from nexa_preprocessing.utils.time_series_operations import slice_by
from sklearn.metrics import classification_report, confusion_matrix

from config import emotion_id_to_emotion, mapper

import numpy as np

df = pd.read_csv("data/full_export.csv")

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

# Specify the path to your JSON file
meta_file_path = "data/meta.json"

# Open and read the JSON file
with open(meta_file_path, 'r') as json_file:
    # Load the JSON data into a Python dictionary
    data_dict = json.load(json_file)


filtered_aliases = []
for s in complete_aliases:
    if s["alias"].isin(data_dict).any():
        filtered_aliases.append(s)


df = pd.concat(filtered_aliases, ignore_index=True)

y_true = df[["emotion_id"]]
y_pred = df[["emotion_id_reply"]]

report = classification_report(y_true, y_pred,
                               target_names=emotion_id_to_emotion.values())

print(report)

conf_matrix = confusion_matrix(y_true, y_pred, normalize="true")

# get emotion_ids
emotion_ids = np.unique(y_true)

# get emotion abreviations
emotion_abrs = mapper(emotion_ids, emotion_id_to_emotion)

# create dataframe with lists of emotion ids as row and column names
df_cm = pd.DataFrame(conf_matrix, list(emotion_abrs), list(emotion_abrs))

# Convert the confusion matrix to a DataFrame for better visualization
conf_matrix_df = pd.DataFrame(conf_matrix, index=range(44), columns=range(44))

turquoise_rgb = (118 / 255, 183 / 255, 178 / 255)
blue_rgb = (78 / 255, 121 / 255, 167 / 255)

# More color definitions
conf_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",
                                                                [(255 / 255, 255 / 255, 215 / 255),
                                                                 turquoise_rgb,
                                                                     blue_rgb])

plt.figure(figsize=(20, 15))
ax = sns.heatmap(df_cm, annot=True, fmt='.1f', vmin=0, vmax=1, cmap=conf_cmap)
plt.yticks(va='center')
plt.xlabel('Predicted Label')
plt.ylabel('Actual Label')
plt.show()