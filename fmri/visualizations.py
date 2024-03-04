import pandas as pd
import chart_studio
import chart_studio.plotly as py
from dotenv import load_dotenv
import os

from utils import create_plotly_conf_mat


load_dotenv()

API_KEY = os.getenv("CHART_STUDIO_API_KEY")

path = "../data/fmri/fmri_audio_export.csv"

df = pd.read_csv(path)

y_true = df[["emotion_1_id"]]
y_pred = df[["reply"]]

fig = create_plotly_conf_mat(y_true, y_pred, title="Confusion Matrix FMRI Audio")

chart_studio.tools.set_credentials_file(username='timlac', api_key=API_KEY)

py.plot(fig, filename='confusion_matrix_fmri_audio', auto_open=True)
