# sequence-alignment

The data consists of 4 separate observations of sequences of motions.  The 4 observations are coded in the “prep” column so 917, 821, etc.  The sequence of interest are given by the “Combo” column. The sequences take place over different types of episodes or epochs listed under “Phase”, “Bout”, and “Moves”.

So the question is what patterns can you find in the Combo sequences (H5M8, H4M3, etc.).  For example, what is the sequence similarity common across Phases, Bouts, Moves and Preps.  What is the variability within these epoch types.  Are there any sequence motifs?

Notes to myself:
What to make of breaks between same epoch types within same prep. For example,
Brace, a type of Move, has interruptions within Prep 917. Should I stitch these
together as one single sequence?

Motif is a region (a subsequence) of protein or DNA sequence that has a specific structure.
Motifs are candidates for functionally important sites.
Presence of a motif may be used as a base of protein classification.
