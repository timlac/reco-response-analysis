import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix
import numpy as np

from nexa_py_sentimotion_mapper.sentimotion_mapper import Mapper


def create_plotly_heatmap(y_true, y_pred):
    emotion_ids = np.unique(y_true)

    conf_matrix = confusion_matrix(y_true, y_pred)

    emotions = Mapper.get_emotion_from_id(emotion_ids)

    # Create the heatmap trace
    heatmap = go.Heatmap(
        z=conf_matrix,
        x=emotions,
        y=emotions,
        colorscale='Blues',  # You can choose other color scales
        # showscale=False,  # Hide the color scale legend
        text=conf_matrix  # Display the values directly in the cells
    )
    return heatmap


def create_plotly_conf_mat(y_true, y_pred, title):
    heatmap = create_plotly_heatmap(y_true, y_pred)

    # Create the layout
    layout = go.Layout(
        title=title,
        xaxis=dict(title="Predicted"),
        yaxis=dict(title="Actual"),
    )

    # Create the figure and display it
    fig = go.Figure(data=[heatmap], layout=layout)

    # Control text formatting
    fig.update_traces(textfont=dict(size=12), texttemplate='%{text:.0f}')

    fig.show()

    return fig
