import pandas as pd
import numpy as np
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
from itertools import combinations
import random
from tqdm import tqdm
import re

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

def makeSequences(df:pd.DataFrame, attr:str):
    """ Make sequences for desired attribute (Prep, Moves, Epochs...). Create
    a dictionary where the key is the sequence name, value 1 the sequence, and
    value 2 the null sequence.
    Args:
        df (pd.DataFrame): Data.
        attr (str): Desired attribute (observations, epochs, etc).
    Returns:
        sequencesDict (dict): Dict with sequence names (keys) and sequences (values)
    """
    frames = [] # create separate frames per observation (ie prep)
    attr_types = df[attr].unique().tolist() # get unique attribute types
    for i in attr_types:
        frames.append(df[df[attr].isin([i])])
    sequencesDict = {}
    for i in range(len(frames)):
        sequences = [] # first element will be full sequence, second full null seq
        sequenceName = str(frames[i][attr].iloc[0])
        sequence = "".join(frames[i]['Sequence'].tolist())
        nullSequence = "".join(frames[i]['SequenceNull'].tolist())
        sequences.append(sequence)
        sequences.append(nullSequence)
        sequencesDict[sequenceName] = sequences

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
    pairs = list(combinations(sequencesDict, 2))
    return pairs


def getGlobalAlignmentScore(pairs:list, sequencesDict:dict, sequenceType:str):
    """ Finds global alignments between pairs, applying
    dynamic programming. Functions comes from:

    https://biopython.org/docs/1.75/api/Bio.pairwise2.html

    Function parameters:
        - Alignment pairs.
        - Identical characters are given 2 points (1 for local alignment)
        - 1 point is deducted for each non-identical character.
        - 0.5 points are deducted when opening a gap (10 for local alignment)
        - 0.1 points are deducted when extending it (0.5 for local alignment).
    Args:
        sequenceType (str): Sequence type name to columns and CSV (ie Prep, etc).
        pairs (list): List of tuples containing sequence pairname combinations.
        sequencesDict (dict): Dictionary containing sequence names as keys,
                              list of sequences as values (1st is sequence,
                              2nd is null sequence).

    """
    aligner = Align.PairwiseAligner()
    results = [] # keep track of results for pd.DataFrame

    for i in tqdm(range(len(pairs)), desc='Global alignments'):
        sequence1Name = pairs[i][0]
        sequence2Name = pairs[i][1]
        sequence1 = sequencesDict[sequence1Name][0]
        sequence2 = sequencesDict[sequence2Name][0]
        sequence1Null = sequencesDict[sequence1Name][1]
        sequence2Null = sequencesDict[sequence2Name][1]
        score = pairwise2.align.globalms(sequence1, sequence2, 2, -1, -.5, -.1, score_only=True)
        score = int(score)

        nullScore = pairwise2.align.globalms(sequence1Null, sequence2Null, 2, -1, -.5, -.1, score_only=True)
        nullScore = int(nullScore)
        normalizedScore = score - nullScore

        scoreResults = {'type':sequenceType, 'pair':pairs[i], 'score':score,
                        'null score':nullScore, 'score normalized':normalizedScore}
        results.append(scoreResults)

        df = pd.DataFrame(results, columns=['type', 'pair', 'score',
                                            'null score', 'score normalized'])
        df.sort_values(by=['score normalized'], ascending=False, inplace=True)
        df.to_csv(sequenceType + '_GlobalResults.csv', index=False)


def getLocalAlignments(pairs:list, sequencesDict:dict, sequenceType:str):
    """Finds local alignments between sequence pairs and builds a dictionary
    containing sequence pair names (keys) and a list of local matches (values).

    https://biopython.org/docs/1.75/api/Bio.pairwise2.html

    Function parameters:
        - Alignment pairs.
        - Identical characters are given 1 point.
        - 1 point is deducted for each non-identical character.
        - 10 points are deducted when opening a gap.
        - 0.5 points are deducted when extending it.
    Args:
        pairs (list): List of tuples containing sequence pairname combinations.
        sequencesDict (dict): Dictionary containing sequence names as keys,
                              list of sequences as values (1st is sequence,
                              2nd is null sequence).
    """
    data_lists = [] # need list of lists for making pd.DataFrame
    for i in tqdm(range(len(pairs)), desc='Local alignments'):
        sequence1Name = pairs[i][0]
        sequence2Name = pairs[i][1]
        sequence1 = sequencesDict[sequence1Name][0]
        sequence2 = sequencesDict[sequence2Name][0]

        for a in pairwise2.align.localms(sequence1, sequence2, 1, -1, -10, -0.5):
            alignment = format_alignment(*a) # returns list of all local alignments
            alignment = alignment.replace('\n', '')
            alignment = alignment.split(' ')
            subsequence = alignment[1]
            score = alignment[len(alignment)-1]
            score = score.split('=')
            score = int(score[1])

            data = []
            data.append(pairs[i])
            data.append(subsequence)
            data.append(score)
        data_lists.append(data)

    df = pd.DataFrame(data_lists, columns=['pair','subsequence', 'score'])
    df.sort_values(by=['score'], ascending=False, inplace=True)
    df.to_csv(sequenceType + '_LocalResults.csv', index=False)


def makeResultsFrames(results:list, sequenceType:str):
    """ Make a pd.DataFrame from alignment results.
    Args:
        results (list): List of dictionaries containing alignment results.
        sequenceType (str): Sequence type name to make CSV.
    Returns:
        None. """
    df_results = pd.DataFrame(results, columns=['type', 'pair', 'score',
                                                'null score', 'score normalized'])
    df_results.sort_values(by=['score normalized'], ascending=False, inplace=True)
    df_results.to_csv(sequenceType + '_results.csv', index=False)
