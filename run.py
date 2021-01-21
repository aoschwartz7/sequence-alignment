from data import *
import pandas as pd

# df_results = pd.read_csv('Prep_results.csv')
# print(df_results)
# #
# #
# exit()
df = pd.read_csv("data.csv") # import sequence data
df = mapASCII(df) # Map sequences to ASCII values for alignments

# Create dictionary of Prep sequences, ie '917.0': 'ASCII_sequence'
sequencesDict = makeSequences(df, 'Bout', 'Sequence')
pairs = makePairs(sequencesDict)
results = globalPairwiseAlign(pairs, sequencesDict, 'Bout')
makeResultsFrame(results)
