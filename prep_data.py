import pandas as pd
import numpy as np
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
import random

df = pd.read_csv("data.csv")

ascii_code = [i for i in range(161,(115+161))] # Create string values from ASCII code

ascii_list = [] # convert code to ASCII symbols
for value in ascii_code:
    ascii_list.append(chr(value))

# Identify unique Combo sequences
unique_combos = df['Combo'].unique()

# Create dictionary for mapping Combo sequences to ASCII
combo_ascii = {unique_combos[i]: ascii_list[i] for i in range(len(unique_combos))}

# Convert Combo column values to map values
df['Combo'] = df['Combo'].map(combo_ascii)

# Shuffle sequences in DataFrame for null testing
df['Combo'] = np.random.permutation(df['Combo'].values)

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

# Create sequences for alignment
seq_prep_115 = Seq(string_prep_115)
seq_prep_821 = Seq(string_prep_821)
seq_prep_917 = Seq(string_prep_917)
seq_prep_925 = Seq(string_prep_925)

# print("Length of Prep115: ", len(seq_prep_115))
# print("Length of Prep821: ", len(seq_prep_821))
# print("Length of Prep917: ", len(seq_prep_917))
# print("Length of Prep925: ", len(seq_prep_925))

# Previous Wolfram parameters (by default): each match between two characters
# contributes +1 to the total similarity score while each mismatch, insertion, or deletion contributes -1.

# I think the only difference between Wolfram and Biopython is that Wolfram
# mentions insertion and deletions deletion as -1 parameters

# Do global alignment (don't penalize gaps)

results = pd.DataFrame(columns = ['Sequences', 'Average Length', 'Score', 'Normalized Score'])
# print(results.head())

seq1 = "ABC"
seq2 = "ABCDEF"

# def getSimilarityScore(results, seq_pair, seq1, seq2):
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

# getSimilarityScore(results, "seq1 x seq2", seq1, seq2)





# prep115x821 = pairwise2.align.globalmx(seq_prep_115, seq_prep_821, match=1, mismatch=-1, score_only=True)
# prep115x917 = pairwise2.align.globalmx(seq_prep_115, seq_prep_917, match=1, mismatch=-1, score_only=True)
# prep115x925 = pairwise2.align.globalmx(seq_prep_115, seq_prep_925, match=1, mismatch=-1, score_only=True)
#
# prep821x917 = pairwise2.align.globalmx(seq_prep_821, seq_prep_917, match=1, mismatch=-1, score_only=True)
# prep821x925 = pairwise2.align.globalmx(seq_prep_821, seq_prep_925, match=1, mismatch=-1, score_only=True)
#
# prep917x925 = pairwise2.align.globalmx(seq_prep_917, seq_prep_925, match=1, mismatch=-1, score_only=True)
#
# print("115x821: ", prep115x821)
# print("115x917: ", prep115x917)
# print("115x925: ", prep115x925)
#
# print("821x917: ", prep821x917)
# print("821x925: ", prep821x925)
#
# print("917x925: ", prep917x925)

# # Test:
# seq1 = "ABCDEF"
# seq2 = "CDABCGHIJKL"
#
# alignment = pairwise2.align.globalmx(seq1, seq2, match=1, mismatch=-1)
# print(alignment)
#
# for a in alignment:
#     print(format_alignment(*a))







# Check lengths of sequences and controls
# print("prep115: ", len(string_prep_115))

# print("prep_115: ", string_prep_115)
# print("***************")
# print("prep_821: ", string_prep_821)
# print("***************")
# print("prep_917: ", string_prep_917)
# print("***************")
# print("prep_925: ", string_prep_925)



# if __name__ == '__main__':
#     ()
