import pandas as pd

# Read the first CSV file
df1 = pd.read_csv('data/like.csv')
df1['Preference'] = '1'

# Read the second CSV file
df2 = pd.read_csv('data/dislike.csv')
df2['Preference'] = '0'

# Concatenate the two dataframes
df = pd.concat([df1, df2])

# Save the combined dataframe to a new CSV file
df.to_csv('data/perfume_preferences.csv', index=False)