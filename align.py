import pandas as pd
import numpy as np
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
from itertools import combinations
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

def makeFrames(df:pd.DataFrame, attr:str):
    """ Make DataFrames for desired attribute (Prep, Moves, Epochs...)
    Args:
        df (pd.DataFrame): Whole dataframe.
        attr (str): Desired attribute (observations, epochs, etc).
    """
    frames = [] # create separate frames per observation (ie prep)
    attr_types = df[attr].unique().tolist() # get unique attribute types

    for i in attr_types:
        frames.append(df[df.Prep.isin([i])]) # TODO: find way to pass in attr for Prep
    return frames


# Focus on Prep data first...
def makePairs(frames:list, attr):
    """ Make Combo sequence pairs for desired frames/attributes.
    Args:
        frames (list): List of separate DataFrames for attribute.
    Returns:
        TODO: Pairwise sequences & pairwise names

    """
    sequencesDict = {}
    for i in range(len(frames)):
        sequenceName = str(frames[i]['Prep'].iloc[0])
        sequence = frames[i]['Combo'].tolist() # combine Combos into single sequence
        sequence = "".join(frames[i]['Combo'].tolist()) # combine Combos into single sequence
        sequencesDict[sequenceName] = sequence
    sequencesList =list(sequencesDict.values())
    # sequencesList = (1,2,3,4)
    makeTuples(sequencesList, sequencesDict)

def makeTuples(sequencesList:list, sequencesDict:dict):
    """ Create tuples of all possible sequence combinations so we can apply
        alignment algorithms below. Helper function for makePairs().
        Args:
            sequencesList (list): Sequences list with just sequences, no keys.
            sequencesDict (list): Dictionary of key-pairs for sequences and their names.
        Returns:
            pairs (list): List of tuples containing all possible sequence pairs.
            pairNames (list): List of matching tuple sequence pair names.
    """
    pairs = list(combinations(sequencesList, 2))
    pairNames = []
    keys = list(sequencesDict.keys())
    vals = list(sequencesDict.values())
    for tup in pairs: # get sequence-pair names
        first = keys[vals.index(tup[0])]
        second = keys[vals.index(tup[1])]
        pairNames.append((first,second))
    return pairs, pairNames


    """ Compares sequence alignment (Combo) among observations (Prep), applying
    Needleman-Wunsch algorithm.
    Args:
        frames (list): List of separate Prep DataFrames
    Returns:
        results...
    """
# def globalAlign(results, seq_pair, seq1, seq2):
#     """ Perform global alignment on sequence combinations and
#     https://biopython.org/docs/1.75/api/Bio.pairwise2.html
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




if __name__ == '__main__':
    frames = makeFrames(df, 'Prep')
    makePairs(frames, 'Prep')
