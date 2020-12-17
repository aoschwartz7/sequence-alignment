import pandas as pd
import numpy as np
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
from itertools import combinations
import random

from Bio import Align

pd.options.mode.chained_assignment = None  # TODO
df = pd.read_csv("data.csv") # import sequence data

def mapASCII(df:pd.DataFrame):
    """ Map sequences to ASCII values for alignments.
    Args:
        df (pd.DataFrame): Data before ASCII mapping.
    Returns:
        df (pd.DataFrame): Data after ASCII mapping, including null sequence column.
    """
    ascii_code = [i for i in range(161,(115+162))] # Create string values from ASCII code
    ascii_list = []
    for value in ascii_code: # Convert ASCII code to ASCII symbols
        ascii_list.append(chr(value))
    del ascii_list[12] # somehow '\xad' is prescent at this index: delete it

    df = df[df['Combo'].notna()] # drop rows where Combo has missing data
    unique_combos = df['Combo'].unique() # identify unique Combo sequences (115 total)

    # Create dictionary for mapping Combo sequences to ASCII
    combo_ascii = {unique_combos[i]: ascii_list[i] for i in range(len(unique_combos))}

    df['Sequence'] = df['Combo'].values
    df['Sequence'] = df['Sequence'].map(combo_ascii) # Map Combo to ascii values    #
    df['SequenceNull'] = np.random.RandomState(seed=1).permutation(df['Sequence'].values) # Shuffle seq for null testing
    return df

def makeSequences(df:pd.DataFrame, attr:str, sequence:str):
    """ Make sequences for desired attribute (Prep, Moves, Epochs...)
    Args:
        df (pd.DataFrame): Data.
        attr (str): Desired attribute (observations, epochs, etc).
        sequence (str): Column name for selecting Sequence or SequenceNull.
    Returns:
        sequencesDict (dict): Dict with sequence names (keys) and sequences (values)
    """
    frames = [] # create separate frames per observation (ie prep)
    attr_types = df[attr].unique().tolist() # get unique attribute types
    for i in attr_types:
        frames.append(df[df[attr].isin([i])])
    sequencesDict = {}
    for i in range(len(frames)):
        sequenceName = str(frames[i][attr].iloc[0])
        eachSequence = frames[i][sequence].tolist() # combine Combos into single sequence
        eachSequence = "".join(frames[i][sequence].tolist()) # combine Combos into single sequence
        sequencesDict[sequenceName] = eachSequence
        sequencesList = list(sequencesDict.values()) # for quick test i'm using this list

    return sequencesDict, sequencesList

def makePairs(sequencesDict:dict):
    """ Make Combo sequence pairs for desired frames/attributes for pairwise-alignments.
    Args:
        sequencesDict (dict): Dict with sequence names (keys) and sequences (values)
    Returns:
        pairs (list): All possible sequence pairs as tuples in list.
        pairNames (list): Names of sequence pairs as tuples in list.
    """
    sequencesList = list(sequencesDict.values())
    pairs, pairNames = makeTuples(sequencesList, sequencesDict)
    return pairs, pairNames

def makeTuples(sequencesList:list, sequencesDict:dict):
    """ Create tuples of all possible sequence combinations so we can apply
        alignment algorithms below. Helper function for makePairs().
        Args:
            sequencesList (list): Sequences list with just sequences, no keys.
            sequencesDict (list): Dictionary of key-pairs for sequences and their names.
        Returns:
            pairs (list): List of tuples containing all possible sequence pairs.
            pairNames (list): List of these tuple sequence pair names.
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

def globalPairwiseAlign(pairs:list, pairNames:list):
    """ Finds global alignment between pairs, applying
    Needleman-Wunsch algorithm (I think). Function comes from:
    https://biopython.org/docs/1.75/api/Bio.pairwise2.html
    Function parameters:
        - Do a global alignment.
        - Identical characters are given 2 points
        - 1 point is deducted for each non-identical character.
        - 0.5 points are deducted when opening a gap
        - 0.1 points are deducted when extending it.
    Args:
        frames (list): List of separate Prep DataFrames
    Returns:
        results...
    """
    aligner = Align.PairwiseAligner()
    aligner.mode = 'local'
    # testing ASCII compatibility
    # alignments = pairwise2.align.globalms(sequencesList[0], sequencesList[1], 2, -1, -.5, -.1)
    alignments = pairwise2.align.globalms(sequencesList[2], sequencesList[3], 2, -1, -.5, -.1, score_only=True)
    print(alignments)
    # x = 0
    # for alignment in sorted(alignments):
    #     if x==2:
    #         break
    #     print("Score = {}".format(alignment.score))
    #     x+=1


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
    df = mapASCII(df)
    sequencesDict, sequencesList = makeSequences(df, 'Prep', 'Sequence')
    pairs, pairNames = makePairs(sequencesDict)
    globalPairwiseAlign(pairs, pairNames)
