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

    if 'nan' in sequencesDict: # remove nan if present
        sequencesDict.pop('nan')

    return sequencesDict


def makePairs(sequencesDict:dict):
    """ Make Combo sequence pairs for desired frames/attributes for pairwise-alignments.
    Args:
        sequencesDict (dict): Dict with sequence names (keys) and sequences (values)
    Returns:
        pairs (list): All possible sequence pairs as tuples in list.
    """
    pairs = list(combinations(sequencesDict, 2)) # limit number combos to pairs (2)
    return pairs


def globalPairwiseAlign(pairs:list, sequencesDict:dict, pairType:str):
    """ Finds best global alignment between pairs, applying
    dynamic programming. Function comes from:
    https://biopython.org/docs/1.75/api/Bio.pairwise2.html
    Function parameters:
        - Do a global alignment.
        - Identical characters are given 2 points
        - 1 point is deducted for each non-identical character.
        - 0.5 points are deducted when opening a gap
        - 0.1 points are deducted when extending it.
    Args:
        pairs (list): List of tuples containing sequence pairname combinations.
        sequencesDict (dict): Dictionary containing sequence names as keys,
                              sequences as values.
    Returns:
        results (list): List containing results as dictionary for a pd.DataFrame.
    """
    aligner = Align.PairwiseAligner()
    dfPairScores = [] # keep track of scores for df
    results = [] # keep track of results for pd.DataFrame
    print("Running alignments.")
    for i in range(len(pairs)): # iterate through tuples and get scores per pair
        sequence1Name = pairs[i][0]
        sequence2Name = pairs[i][1]
        sequence1 = sequencesDict[sequence1Name]
        sequence2 = sequencesDict[sequence2Name]
        alignmentScore = pairwise2.align.globalms(sequence1, sequence2, 2, -1, -.5, -.1, score_only=True)
        alignmentScore = int(alignmentScore)
        scoreResults = {'type':pairType, 'pair':pairs[i], 'score':alignmentScore}
        print(scoreResults)
        results.append(scoreResults)
    return results

def makeResultsFrame(results:list):
    """ Make a pd.DataFrame from alignment results. """
    df_results = pd.DataFrame(results, columns=['type', 'pair', 'score'])
    df_results.sort_values(by=['score'], ascending=False, inplace=True)
    df_results.to_csv('Bout_results.csv', index=False)
