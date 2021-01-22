from data import *
import pandas as pd

# 'Bout', 'Phase', 'Prep'
sequenceType = 'Prep' # TODO: find better way to run this code

df = pd.read_csv("data.csv") # import sequence data
# print(df)
# exit()
df = mapASCII(df) # Map sequences to ASCII values for alignments

# Create dictionary of Prep sequences, ie '917.0': 'ASCII_sequence'
sequencesDict = makeSequences(df, sequenceType)
pairs = makePairs(sequencesDict)
getGlobalAlignmentScore(pairs, sequencesDict, sequenceType)
getLocalAlignments(pairs, sequencesDict, sequenceType)
# makeResultsFrames(results, sequenceType)
