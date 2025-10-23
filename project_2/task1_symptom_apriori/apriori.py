import pandas as pd
import itertools

df = pd.read_csv("../data/cleaned/dataset_cleaned.csv")
print(df.columns)

df['Symptoms'] = df['Symptoms'].apply(lambda x: x.split(';'))
transactions= df['Symptoms'].tolist()

min_transactions = 1000 # if too few transactions, mirror them
if len(transactions) < min_transactions:
    transactions = transactions * (min_transactions // len(transactions) + 1)


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
      support= count/num_tx
      item_supp[i]=support
      #print(i, count, supp) # to print the support
    
    # 3. iteratively build larger itemsets
    freq_items_L1={}
    for i in item_supp:
      if(item_supp[i]>= min_support):
        freq_items_L1[frozenset([i])]= item_supp[i]
    freq_items_Ln=freq_items_L1.copy()
    all_frequent_items = dict(freq_items_L1) # all itemsets discovered
    n=2
    still_candidates= True
    while still_candidates:
      #candidates= itertools.combinations(list(freq_items_Ln.keys()),n)
      prev_freq = list(freq_items_Ln.keys())
      candidates = []
      for a, b in itertools.combinations(prev_freq, 2):
        merged = a.union(b)
        if len(merged) == n:  # only keep itemsets of size n
          candidates.append(merged)
      freq_items_Lnext = {}
      for i in candidates:
        count=0
        for j in transactions:
          if(i.issubset(j)):
            count+=1
        # 2. prune those below threshold
        support=count/len(transactions)
        if support>= min_support:
          freq_items_Lnext[i]= support
        #print(freq_items_Ln)
      freq_items_Ln = freq_items_Lnext
      all_frequent_items.update(freq_items_Ln)

      #check if there are still new candidates
      if freq_items_Ln:          #if not empty
        n+=1
      else: still_candidates= False

    # return list of frequent itemsets with support values
    #return all_frequent_items
    return dict(sorted(all_frequent_items.items(), key=lambda x: (len(x[0]), -x[1]))) #return sorted itemsets instead

def make_rules(frequent_itemsets, min_confidence):
  rules = []
  for itemset, supp in frequent_itemsets.items():
      if len(itemset) >= 2:
          for prev in itertools.chain.from_iterable(
              itertools.combinations(itemset, r) for r in range(1, len(itemset))
          ):
              prev = frozenset(prev)
              consequent = itemset - prev
              if consequent:
                  conf = supp / frequent_itemsets.get(prev, 1)
                  if conf >= min_confidence:
                      rules.append((prev, consequent, supp, conf))
  return rules


result = apriori(0.1, transactions)

# print(f"Number of frequent itemsets: {len(result)}")
# for items, support in result.items():
#     print(set(items), ":", round(support, 3))

rules = make_rules(result, min_confidence=0.7)
print(f"Number of rules: {len(rules)}")
for antecedent, consequent, support, confidence in rules:
    print(f"{set(antecedent)} -> {set(consequent)}, support: {round(support,3)}, confidence: {round(confidence,3)}")