import pandas as pd
import pingouin as pg

# Sample data: 5 subjects, measured by 3 different raters
data = {
    "Rater1": [1.2, 2.3, 3.1, 4.4, 5.2],
    "Rater2": [1.1, 2.4, 3.0, 4.5, 5.1],
    "Rater3": [1.2, 2.5, 3.2, 4.4, 5.3]
}

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Melt the DataFrame so it's in long format for the ICC calculation
df_melt = df.melt(var_name='Rater', value_name='Measurement')

# Add a 'Subject' column to indicate which measurements belong to which subject
df_melt['Subject'] = df_melt.index // 3 + 1

# Calculate the ICC
icc = pg.intraclass_corr(data=df_melt, targets='Subject', raters='Rater', ratings='Measurement').round(3)

# Print the ICC result
print(icc)