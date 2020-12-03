import pandas as pd
import numpy as np
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
import random

df = pd.read_csv("data.csv") # sequence data

ascii_code = [i for i in range(161,(115+161))] # Create string values from ASCII code

ascii_list = [] # convert code to ASCII symbols
for value in ascii_code:
    ascii_list.append(chr(value))


unique_combos = df['Combo'].unique() # Identify unique Combo sequences


# Create dictionary for mapping Combo sequences to ASCII
combo_ascii = {unique_combos[i]: ascii_list[i] for i in range(len(unique_combos)-1)}

df['Combo'] = df['Combo'].map(combo_ascii) # Convert Combo column values to map values
df['Combo'] = np.random.RandomState(seed=33).permutation(df['Combo'].values) # shuffle seq for null testing

# dataframe_collection = {}
# for month_day in month_day_list:
#     new_data = np.random.rand(3,3)
#     dataframe_collection[month_day] = pd.DataFrame(new_data, columns=["one", "two", "three"])

df_obs = {} # empty dict we will fill with dataframes separated by Observations/Preps
obs = ['115', '821', '917', '925']
epochs = ['Phase', 'Bout', 'Moves']


# def split_obs(dfs:dict, df:pd.DataFrame, obs:list, epochs:list):
def split_obs(df_obs:dict, df:pd.DataFrame, obs:list):
    """ Split each observation (115, 821, 917, 925) into separate DataFrames.
        Append each df to dfs[].
    Args:
        df_obs (dict): Empty dict.
        df (pd.DataFrame): source dataframe.
        obs (list): list containing the 4 observations to capture.
    Returns:
        df_obs (dict): Dictionary now containing 4 DataFrames.
    """
    for i in obs:
        df_new = df[df.Prep.isin([i])]
        df_obs[i] = df_new
    return df_obs

# def get_sequences(dfs:dict):
#     a



if __name__ == '__main__':
    split_obs(df_obs, df, obs)

# Create list of Combo sequences for each Prep
# combo_list_prep_115 = df_115['Combo'].tolist()
# combo_list_prep_821 = df_821['Combo'].tolist()
# combo_list_prep_917 = df_917['Combo'].tolist()
# combo_list_prep_925 = df_925['Combo'].tolist()
#
# # Convert Combo sequence lists to single string
# string_prep_115 = ''.join(combo_list_prep_115)
# string_prep_821 = ''.join(combo_list_prep_821)
# string_prep_917 = ''.join(combo_list_prep_917)
# string_prep_925 = ''.join(combo_list_prep_925)
#
# # Create sequences for alignment
# seq_prep_115 = Seq(string_prep_115)
# seq_prep_821 = Seq(string_prep_821)
# seq_prep_917 = Seq(string_prep_917)
# seq_prep_925 = Seq(string_prep_925)
# print(df_115.head)
