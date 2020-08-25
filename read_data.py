import pandas as pd

df = pd.read_csv("data.csv")
print(df.head(10))

# Create string values from ASCII code
ascii_code = [i for i in range(161,(115+161))]

ascii_list = []
for value in ascii_code:
    ascii_list.append(chr(value))

# Identify unique Combo sequences
unique_combos = df['Combo'].unique()

# Create dictionary for mapping Combo sequences to ASCII
combo_ascii = {unique_combos[i]: ascii_list[i] for i in range(len(unique_combos))}

# Convert Combo column values to map values
df['Combo'] = df['Combo'].map(combo_ascii)

# Create Combo sequences for each Observation
df_115 = df[df.Prep.isin(['115'])]
df_821 = df[df.Prep.isin(['821'])]
df_917 = df[df.Prep.isin(['917'])]
df_925 = df[df.Prep.isin(['925'])]

# How many elements per Observation?
# print("Number of Combo elements in Obs 115: {} ".format(len(df_115)))
# print("Number of Combo elements in Obs 821: {} ".format(len(df_821)))
# print("Number of Combo elements in Obs 917: {} ".format(len(df_917)))
# print("Number of Combo elements in Obs 925: {} ".format(len(df_925)))

# Create list of Combo sequences for each Prep
combo_list_prep_115 = df_115['Combo'].tolist()
combo_list_prep_821 = df_821['Combo'].tolist()
combo_list_prep_917 = df_917['Combo'].tolist()
combo_list_prep_925 = df_925['Combo'].tolist()

# Convert Combo sequence lists to single string
string_prep_115 = ''.join(combo_list_prep_115)
string_prep_821 = ''.join(combo_list_prep_821)
string_prep_917 = ''.join(combo_list_prep_917)
string_prep_925 = ''.join(combo_list_prep_925)


# print("prep_115: ", string_prep_115)
# print("***************")
# print("prep_821: ", string_prep_821)
# print("***************")
# print("prep_917: ", string_prep_917)
# print("***************")
# print("prep_925: ", string_prep_925)
