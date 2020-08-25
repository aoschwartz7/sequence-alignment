import pandas as pd

df = pd.read_csv("data.csv")

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

# How many unique Phases?
unique_phases = df['Phase'].unique()
# 'S' 'P1' 'P2' 'T' 'P3'

# # Create Combo sequences for each Phase
df_S = df[df.Phase.isin(['S'])]
df_T = df[df.Phase.isin(['T'])]
df_P1 = df[df.Phase.isin(['P1'])]
df_P2 = df[df.Phase.isin(['P2'])]
df_P3 = df[df.Phase.isin(['P3'])]

# How many elements per Phase?
# print("Number of Phase elements in Phase S: {} ".format(len(df_S)))
# print("Number of Phase elements in Phase T: {} ".format(len(df_T)))
# print("Number of Phase elements in Phase P1: {} ".format(len(df_P1)))
# print("Number of Phase elements in Phase P2: {} ".format(len(df_P2)))
# print("Number of Phase elements in Phase P3: {} ".format(len(df_P3)))


# Create list of Combo sequences for each Phase
combo_list_phase_S = df_S['Combo'].tolist()
combo_list_phase_T = df_T['Combo'].tolist()
combo_list_phase_P1 = df_P1['Combo'].tolist()
combo_list_phase_P2 = df_P2['Combo'].tolist()
combo_list_phase_P3 = df_P3['Combo'].tolist()

# Convert Combo sequence lists to single string
string_phase_S = ''.join(combo_list_phase_S)
string_phase_T = ''.join(combo_list_phase_T)
string_phase_P1 = ''.join(combo_list_phase_P1)
string_phase_P2 = ''.join(combo_list_phase_P2)
string_phase_P3 = ''.join(combo_list_phase_P3)

# Check length of conversion before and after:
# print("Phase_S before and after: ", len(df_S), " ", len(string_phase_S))
# print("Phase_T before and after: ", len(df_T), " ", len(string_phase_T))
# print("Phase_P1 before and after: ", len(df_P1), " ", len(string_phase_P1))
# print("Phase_P2 before and after: ", len(df_P2), " ", len(string_phase_P2))
# print("Phase_P3 before and after: ", len(df_P3), " ", len(string_phase_P3))



print("phaseS: ", string_phase_S)
print("***************")
print("phaseT: ", string_phase_T)
print("***************")
print("phaseP1: ", string_phase_P1)
print("***************")
print("phaseP2: ", string_phase_P2)
print("***************")
print("phaseP3: ", string_phase_P3)
