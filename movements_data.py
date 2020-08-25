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

# How many unique Moves?
unique_moves = df['Moves'].unique()
print(unique_moves)
# [nan 'Lift' 'Dgap' 'Brace' 'Swing' 'Crunch' 'AntComp' 'BotSwing' 'Pgap']

# Create Combo sequences for each Movement
df_Lift = df[df.Moves.isin(['Lift'])]
df_Dgap = df[df.Moves.isin(['Dgap'])]
df_Brace = df[df.Moves.isin(['Brace'])]
df_Swing = df[df.Moves.isin(['Swing'])]
df_Crunch = df[df.Moves.isin(['Crunch'])]
df_AntComp = df[df.Moves.isin(['AntComp'])]
df_BotSwing = df[df.Moves.isin(['BotSwing'])]
df_Pgap = df[df.Moves.isin(['Pgap'])]


# How many elements per Movement?
# print("Number of Movement elements in Lift: {} ".format(len(df_Lift)))
# print("Number of Movement elements in Dgap: {} ".format(len(df_Dgap)))
# print("Number of Movement elements in Brace: {} ".format(len(df_Brace)))
# print("Number of Movement elements in Swing: {} ".format(len(df_Swing)))
# print("Number of Movement elements in Crunch: {} ".format(len(df_Crunch)))
# print("Number of Movement elements in AntComp: {} ".format(len(df_AntComp)))
# print("Number of Movement elements in BotSwing: {} ".format(len(df_BotSwing)))
# print("Number of Movement elements in Pgap: {} ".format(len(df_Pgap)))


# Create list of Combo sequences for each Movement
combo_list_move_Lift = df_Lift['Combo'].tolist()
combo_list_move_Dgap = df_Dgap['Combo'].tolist()
combo_list_move_Brace = df_Brace['Combo'].tolist()
combo_list_move_Swing = df_Swing['Combo'].tolist()
combo_list_move_Crunch = df_Crunch['Combo'].tolist()
combo_list_move_AntComp = df_AntComp['Combo'].tolist()
combo_list_move_BotSwing = df_BotSwing['Combo'].tolist()
combo_list_move_Pgap = df_Pgap['Combo'].tolist()

# Convert Combo sequence lists to single string
string_move_Lift = ''.join(combo_list_move_Lift)
string_move_Dgap = ''.join(combo_list_move_Dgap)
string_move_Brace = ''.join(combo_list_move_Brace)
string_move_Swing = ''.join(combo_list_move_Swing)
string_move_Crunch = ''.join(combo_list_move_Crunch)
string_move_AntComp = ''.join(combo_list_move_AntComp)
string_move_BotSwing = ''.join(combo_list_move_BotSwing)
string_move_Pgap = ''.join(combo_list_move_Pgap)


# Check length of conversion before and after:
# print("move_Lift before and after: ", len(df_Lift), " ", len(string_move_Lift))
# print("move_Dgap before and after: ", len(df_Dgap), " ", len(string_move_Dgap))
# print("move_Brace before and after: ", len(df_Brace), " ", len(string_move_Brace))
# print("move_Swing before and after: ", len(df_Swing), " ", len(string_move_Swing))
# print("move_Crunch before and after: ", len(df_Crunch), " ", len(string_move_Crunch))
# print("move_AntComp before and after: ", len(df_AntComp), " ", len(string_move_AntComp))
# print("move_BotSwing before and after: ", len(df_BotSwing), " ", len(string_move_BotSwing))
# print("move_Pgap before and after: ", len(df_Pgap), " ", len(string_move_Pgap))




print("Move Lift: ", string_move_Lift)
print("***************")
print("Move Dgap: ", string_move_Dgap)
print("***************")
print("Move Brace: ", string_move_Brace)
print("***************")
print("Move Swing: ", string_move_Swing)
print("***************")
print("Move Crunch: ", string_move_Crunch)
print("***************")
print("Move AntComp: ", string_move_AntComp)
print("***************")
print("Move BotSwing: ", string_move_BotSwing)
print("***************")
print("Move Pgap: ", string_move_Pgap)
print("***************")
