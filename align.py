import pandas as pd
import numpy as np
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
import random

df = pd.read_csv("data.csv") # import sequence data as DataFrame



ascii_code = [i for i in range(161,(115+162))] # Create string values from ASCII code
# ascii_code = [i for i in range(128,130)]
ascii_list = []
for value in ascii_code: # Convert ASCII code to ASCII symbols
    ascii_list.append(chr(value))

del ascii_list[12] # somehow '\xad' is prescent at this index: delete it

df = df[df['Combo'].notna()] # drop rows where Combo has missing data
unique_combos = df['Combo'].unique() # identify unique Combo sequences (115 total)

# Create dictionary for mapping Combo sequences to ASCII
combo_ascii = {unique_combos[i]: ascii_list[i] for i in range(len(unique_combos))}

df['Combo'] = df['Combo'].map(combo_ascii) # Map Combo to ascii values
df['ComboNull'] = np.random.RandomState(seed=1).permutation(df['Combo'].values) # Shuffle seq for null testing

frames = [] # create separate frames per observation (ie prep)
obs = df['Prep'].unique().tolist() # get unique observations
moves = df['Moves'].unique().tolist()

for i in obs:
    frames.append(df[df.Prep.isin([i])])

def comparePrep(frames:list):
    """ Compares sequence alignment (Combo) among observations (Prep), applying
    Needleman-Wunsch algorithm.
    Args:
        frames (list): List of separate Prep DataFrames
    Returns:
        results...
    """
    sequences = {}
    for i in range(len(frames)):
        sequenceName = str(frames[i]['Prep'].iloc[0])
        sequence = frames[i]['Combo'].tolist() # combine Combos into single sequence
        sequence = "".join(frames[i]['Combo'].tolist()) # combine Combos into single sequence
        sequences[sequenceName] = sequence


def makeTuples():
    """ Create tuples of all possible sequence combinations.
    """


# def globalAlign(results, seq_pair, seq1, seq2):
#     """ Perform global alignment on sequence combinations and
#     """
#     score = pairwise2.align.globalmx(seq1, seq2, match=1, mismatch=-1, score_only=True)
#     avg_length = (len(seq1)+len(seq2))/2
#     normalized_score = score/(avg_length)
#
#     # print(seq_pair, avg_length, score, normalized_score)
#     new_row = pd.Series(
#           data={
#                'Sequences':[seq_pair],
#                'Average Length':[avg_length],
#                'Score':[score],
#                'Normalized Score':[normalized_score]
#                },
# ...       index=df.columns, name=17)
#
#     new_row = {'Sequences':[seq_pair],
#                'Average Length':[avg_length],
#                'Score':[score],
#                'Normalized Score':[normalized_score]}
#     data = pd.DataFrame(new_row)
#     df = df.append(data)

    # generate each Combo sequence per Prep as key-value pair






epochs = ['Phase', 'Bout', 'Moves']


# def split_obs(dfs:dict, df:pd.DataFrame, obs:list, epochs:list):
# def split_obs(df_obs:dict, df:pd.DataFrame, obs:list):
#     """ Split each observation (115, 821, 917, 925) into separate DataFrames.
#         Append each df to dfs[].
#     Args:
#         df_obs (dict): Empty dict.
#         df (pd.DataFrame): source dataframe.
#         obs (list): list containing the 4 observations to capture.
#     Returns:
#         df_obs (dict): Dictionary now containing 4 DataFrames.
#     """
#     for i in obs:
#         df_new = df[df.Prep.isin([i])]
#         df_obs[i] = df_new
#     return df_obs

# def get_sequences(dfs:dict):
#     a



if __name__ == '__main__':
    comparePrep(frames)
#     split_obs(df_obs, df, obs)

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
