import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
import numpy as np
from itertools import combinations, chain
from collections import defaultdict

#It is either "B" or "M", we will run GSP only on the patient who have the malignant disease or the one where they only have the benign disease for B


#Top K 
TOP_K = 10

df = pd.read_csv("../data/raw/Cancer_Data.csv")


"""
Sort the features by z-score in descending order and return the top K features
"""
def top_k_features_by_z(row,top_k):
    return row.sort_values(ascending=False).index.tolist()[:top_k]


df_zscore = df.iloc[:, 2:-1].copy()

features = df_zscore.columns


for feature in features:
    df_zscore[feature] = abs((df[feature] - df[feature].mean()) / df[feature].std())


#top_K features for each patient
ordered_features = df_zscore.apply(top_k_features_by_z, axis=1, top_k=TOP_K)

# Feature discretization using KBinsDiscretizer
BINNING_STRATEGY = "quantile"   
N_BINS = 3                      #categories: low, medium, high
bin_labels = {0: "low", 1: "medium", 2: "high"}


kbd = KBinsDiscretizer(n_bins=N_BINS, encode='ordinal', strategy=BINNING_STRATEGY)
 

df_binned = pd.DataFrame(
    kbd.fit_transform(df_zscore),
    columns=df_zscore.columns,
    index=df_zscore.index
)

patient_sequences = []

for idx, row in df_zscore.iterrows():
    top_feats = ordered_features[idx]  # top-K features for this patient
    sequence = []
    i = 0
    
    #We implement this logic to have feature ties in the same itemset
    while i < len(top_feats):
        current_itemset = set()
        current_feature = top_feats[i]
        current_score = row[current_feature]
        
        # Add the first feature to the itemset
        bin_index = df_binned.loc[idx, current_feature]
        current_itemset.add(f"{bin_labels[bin_index]}_{current_feature}")
        
        # Look ahead to find ties
        j = i + 1
        while j < len(top_feats) and np.isclose(row[top_feats[j]], current_score):
            tie_feature = top_feats[j]
            bin_index = df_binned.loc[idx, tie_feature]
            current_itemset.add(f"{bin_labels[bin_index]}_{tie_feature}")
            j += 1
        
        # Append the itemset and move the pointer past the ties
        sequence.append(current_itemset)
        i = j
    
    patient_sequences.append(sequence)    







def gsp_dp(sequences, min_support, max_pattern_len):
    """
    Optimized GSP using prefix-based pruning for faster sequential pattern mining.
    
    sequences: list of list of items (e.g., patient sequences)
    min_support: minimum number of sequences a pattern must appear in
    max_pattern_len: maximum length of sequence to consider
    """
    
    # Step 1: Count frequent 1-item patterns
    freq_patterns = dict()
    candidates = defaultdict(int)
    
    for seq in sequences:
        for item in seq:
            candidates[(item,)] += 1
    
    # Keep only frequent 1-item patterns
    freq_patterns[1] = {k: v for k, v in candidates.items() if v >= min_support}
    
    print(f"Found {len(freq_patterns[1])} frequent 1-item patterns")
    
    k = 2
    while k <= max_pattern_len and freq_patterns.get(k-1):
        
        print(f"\n=== Generating candidates of length {k} ===")
        prev_freq = list(freq_patterns[k-1].keys())
        candidates = defaultdict(int)
        
        # Prefix-based join: join only sequences with same first k-2 items
        for i in range(len(prev_freq)):
            for j in range(i+1, len(prev_freq)):
                # Only join if first k-2 items are equal
                if prev_freq[i][:-1] == prev_freq[j][:-1]:
                    candidate = prev_freq[i] + (prev_freq[j][-1],)
                    # Count support efficiently
                    support = 0
                    for seq in sequences:
                        idx = 0
                        for item in candidate:
                            while idx < len(seq) and seq[idx] != item:
                                idx += 1
                            if idx == len(seq):
                                break
                            idx += 1
                        else:
                            support += 1

                        
                    if support >= min_support:
                        candidates[candidate] = support
        
        freq_patterns[k] = dict(candidates)
        print(f"Found {len(freq_patterns[k])} frequent patterns of length {k}")
        k += 1
        
    return freq_patterns

#We convert them to frozenset so it is immutable and hashable
# Split sequences for B and M
patient_sequences_B = [
    [frozenset(itemset) for itemset in seq]
    for idx, seq in enumerate(patient_sequences)
    if df.loc[idx, "diagnosis"] == "B"
]

patient_sequences_M = [
    [frozenset(itemset) for itemset in seq]
    for idx, seq in enumerate(patient_sequences)
    if df.loc[idx, "diagnosis"] == "M"
]



min_support = 15  # pattern must appear in at least 2 patients
max_pattern_len = 10

frequent_patterns_M = gsp_dp(patient_sequences_M, min_support=min_support, max_pattern_len=max_pattern_len)
frequent_patterns_B = gsp_dp(patient_sequences_B, min_support=min_support, max_pattern_len=max_pattern_len)

# Print top patterns 
"""
for k, patterns in frequent_patterns_M.items():
    print(f"=== Frequent patterns of length {k} ===")
    for pat, sup in patterns.items():
        
        pretty_str = ", ".join(
            "{" + ", ".join(pattern) + "}"
            for pattern in pat
        )
        print(pretty_str, " -> ", sup)
"""

def compare_patterns(freq_B, freq_M):
    comparison = []
    all_patterns = set()
    for d in [freq_B, freq_M]:
        for k, patterns in d.items():
            all_patterns.update(patterns.keys())
    
    for pat in all_patterns:
        sup_B = sum(freq_B.get(len(pat), {}).get(pat, 0) for _ in [0])
        sup_M = sum(freq_M.get(len(pat), {}).get(pat, 0) for _ in [0])
        comparison.append((pat, sup_B, sup_M))
    return comparison

pattern_comparison = compare_patterns(frequent_patterns_B, frequent_patterns_M)

print("\n=== Pattern comparison (B vs M) ===")
for pat, sup_B, sup_M in pattern_comparison:
    pretty_str = ", ".join("{" + ", ".join(itemset) + "}" for itemset in pat)
    print(f"{pretty_str} | B: {sup_B}, M: {sup_M}")
