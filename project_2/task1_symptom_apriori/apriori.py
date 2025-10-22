import pandas as pd

df = pd.read_csv("../data/cleaned/dataset_cleaned.csv")
print(df.columns)

df['Symptoms'] = df['Symptoms'].apply(lambda x: x.split(';'))
transactions= df['Symptoms'].tolist()

# print(f"Total transactions: {len(transactions)}")
# print("Example transaction:", transactions[0])

def apriori (min_support, transactions):
    # 1. count individual items
    
    all_symptoms=set()
    for i in transactions:
      all_symptoms.update(i)
    #print(all_symptoms)

    all_items={}
    for i in all_symptoms:
      count=0
      for j in transactions:
        if i in j:
          count+=1
      all_items[i]=count
    
    # convert count to support
    num_tx= len(transactions)
    item_supp={}

    for i, count in all_items.items():
      supp= count/num_tx
      item_supp[i]=supp
      #print(i, count, supp) # to print the support
    
  

    # 2. prune those below threshold
    freq_items_L1={}
    for i in item_supp:
      if(item_supp[i]>= min_support):
        freq_items_L1[frozenset([i])]= item_supp[i]
    print(freq_items_L1)

    # 3. iteratively build larger itemsets
    while():
      

    # return list of frequent itemsets with support values

apriori(0.2, transactions)
