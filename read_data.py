import pandas as pd

df = pd.read_csv("data.csv")

# Identify uniques
# unique_combos = df['Combo'].value_counts()
# # Combo, Length: 115
# print(unique_combos)
#
# unique_phases = df['Phase'].value_counts()
# print(unique_phases)
#
# unique_prep = df['Prep'].value_counts()
# print(unique_prep)


# Create dataframes for each Observation
df_115 = df[df.Prep.isin(['115'])]
df_821 = df[df.Prep.isin(['821'])]
df_917 = df[df.Prep.isin(['917'])]
df_925 = df[df.Prep.isin(['925'])]

# How many elements per Observation?
print("Number of Combo elements in Obs 115: {} ".format(len(df_115)))
print("Number of Combo elements in Obs 821: {} ".format(len(df_821)))
print("Number of Combo elements in Obs 917: {} ".format(len(df_917)))
print("Number of Combo elements in Obs 925: {} ".format(len(df_925)))

# Create list of Combo sequences for each Observation
combo_list_obs_115 = df_115['Combo'].tolist()
combo_list_obs_821 = df_821['Combo'].tolist()
combo_list_obs_917 = df_917['Combo'].tolist()
combo_list_obs_925 = df_925['Combo'].tolist()

# Convert Combo sequence lists to single string
string_obs_115 = ''.join(combo_list_obs_115)
string_obs_821 = ''.join(combo_list_obs_821)
string_obs_917 = ''.join(combo_list_obs_917)
string_obs_925 = ''.join(combo_list_obs_925)
