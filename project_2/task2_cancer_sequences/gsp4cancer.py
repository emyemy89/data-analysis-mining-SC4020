import pandas as pd

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


df_zscore = df.iloc[:, 2:].copy()

features = df_zscore.columns


for feature in features:
    df_zscore[feature] = abs((df[feature] - df[feature].mean()) / df[feature].std())

#top_K features for each patient
ordered_features = df_zscore.apply(top_k_features_by_z, axis=1, top_k=TOP_K)




print(ordered_features.head())



