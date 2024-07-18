import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt

from nexa_preprocessing.utils.time_series_operations import slice_by, get_identifier_vals_as_array

path = "../../data/appraisal/export_appraisal_main_study.csv"

df = pd.read_csv(path)

slices = slice_by(df, "survey_id")
survey_ids = get_identifier_vals_as_array(slices, "survey_id")
user_ids = get_identifier_vals_as_array(slices, "user_id")


scales = [
    'reply_dim_Novelty',
    'reply_dim_Pleasantness',
    'reply_dim_Goal conduciveness',
    'reply_dim_Urgency',
    'reply_dim_Power',
    'reply_dim_Norm compatibility'
]

results = {}

residuals = []
f_scores = []
p_values = []

for idx, df_slice in enumerate(slices):

    model = ols(f"{scales[1]} ~ C(emotion_1)", data=df_slice).fit()
    anova_results = sm.stats.anova_lm(model, typ=2)

    results[survey_ids[idx]] = anova_results

    residual = anova_results["sum_sq"]["Residual"]
    f_score = anova_results["F"]["C(emotion_1)"]
    p_value = anova_results["PR(>F)"]["C(emotion_1)"]

    print()
    # print(f"Sum time spent: {df_slice['time_spent_on_item'].sum()}")
    print(f"user id: {user_ids[idx]}")
    print(f"survey_id: {survey_ids[idx]}")
    print(f"anova_results: {anova_results}")

    residuals.append(residual)
    f_scores.append(f_score)
    p_values.append(p_value)


# Normalizing function
def normalize(data):
    return (data - min(data)) / (max(data) - min(data))


x = list(range(1, len(slices) + 1))

print(len(f_scores))

plt.hist(p_values, bins=29)

# # Create the plot
# plt.plot(x, normalize(residuals), label='Residuals')
# plt.plot(x, normalize(f_scores), label='F scores')
# plt.plot(x, normalize(p_values), label='P Values')
#
# # Adding a title
# plt.title('Multiple Line Plot')
#
# # Adding labels
# plt.xlabel('X axis')
# plt.ylabel('Y axis')
#
# # Adding a legend
# plt.legend()

# Show the plot
plt.show()
