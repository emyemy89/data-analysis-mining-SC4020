import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
import numpy as np

"""
Next thing to do, is for each row, having the top K features, transform them into their values, and convert the numerical values into categorical values with KBinsDiscretizer (uniform / quantile / k-means) 


"""


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

