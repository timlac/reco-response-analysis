import matplotlib
import pandas as pd
import json
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


from matplotlib import pyplot as plt
from nexa_preprocessing.utils.time_series_operations import slice_by
from sklearn.metrics import classification_report, confusion_matrix

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


# fig = px.imshow(df_cm, text_auto=True)
# fig.update_layout(title="Confusion Matrix", xaxis_title="Predicted", yaxis_title="Actual")
# fig.show()

# Create the heatmap trace
heatmap = go.Heatmap(
    z=conf_matrix,
    x=emotion_abrs,
    y=emotion_abrs,
    colorscale='Blues',  # You can choose other color scales
    # showscale=False,  # Hide the color scale legend
    text=conf_matrix  # Display the values directly in the cells
)

# Create the layout
layout = go.Layout(
    title="Confusion Matrix",
    xaxis=dict(title="Predicted"),
    yaxis=dict(title="Actual"),
)

# Create the figure and display it
fig = go.Figure(data=[heatmap], layout=layout)

# Control text formatting
fig.update_traces(textfont=dict(size=12), texttemplate='%{text:.1f}')

fig.show()