"""
Apriori Algorithm for Symptom Association Rule Mining
Mines frequent symptom combinations and association rules from disease data
"""

import pandas as pd
import numpy as np
from itertools import combinations
from collections import defaultdict
import json

class AprioriMiner:
    def __init__(self, min_support=0.05, min_confidence=0.6):
        """
        Initialize Apriori miner
        
        Args:
            min_support: Minimum support threshold (0-1)
            min_confidence: Minimum confidence threshold for rules (0-1)
        """
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = {}
        self.association_rules = []
        self.disease_symptom_rules = {}
        
    def get_transactions(self, df):
        """Convert DataFrame to transaction format"""
        transactions = []
        for _, row in df.iterrows():
            symptoms = row['Symptoms'].split(';')
            symptoms = [s.strip() for s in symptoms]
            transactions.append(set(symptoms))
        return transactions
    
    def calculate_support(self, itemset, transactions):
        """Calculate support for an itemset"""
        count = sum(1 for transaction in transactions if itemset.issubset(transaction))
        return count / len(transactions)
    
    def get_frequent_1_itemsets(self, transactions):
        """Find frequent 1-itemsets"""
        item_counts = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                item_counts[item] += 1
        
        n_transactions = len(transactions)
        frequent_items = {}
        
        for item, count in item_counts.items():
            support = count / n_transactions
            if support >= self.min_support:
                frequent_items[frozenset([item])] = support
        
        return frequent_items
    
    def apriori_gen(self, prev_frequent, k):
        """Generate candidate k-itemsets from (k-1)-itemsets"""
        candidates = set()
        prev_items = list(prev_frequent.keys())
        
        for i in range(len(prev_items)):
            for j in range(i + 1, len(prev_items)):
                # Join step: merge two (k-1)-itemsets
                union = prev_items[i] | prev_items[j]
                if len(union) == k:
                    # Prune step: all (k-1)-subsets must be frequent
                    subsets = [frozenset(s) for s in combinations(union, k-1)]
                    if all(subset in prev_frequent for subset in subsets):
                        candidates.add(union)
        
        return candidates
    
    def mine_frequent_itemsets(self, transactions, max_length=4):
        """Mine all frequent itemsets up to max_length"""
        print("Mining frequent itemsets...")
        
        # Get frequent 1-itemsets
        self.frequent_itemsets[1] = self.get_frequent_1_itemsets(transactions)
        print(f"Found {len(self.frequent_itemsets[1])} frequent 1-itemsets")
        
        k = 2
        while k <= max_length:
            # Generate candidates
            candidates = self.apriori_gen(self.frequent_itemsets[k-1], k)
            
            if not candidates:
                break
            
            # Calculate support for candidates
            frequent_k = {}
            for candidate in candidates:
                support = self.calculate_support(candidate, transactions)
                if support >= self.min_support:
                    frequent_k[candidate] = support
            
            if not frequent_k:
                break
            
            self.frequent_itemsets[k] = frequent_k
            print(f"Found {len(frequent_k)} frequent {k}-itemsets")
            k += 1
        
        return self.frequent_itemsets
    
    def generate_association_rules(self):
        """Generate association rules from frequent itemsets"""
        print("\nGenerating association rules...")
        self.association_rules = []
        
        # For each frequent itemset of size >= 2
        for k in range(2, max(self.frequent_itemsets.keys()) + 1):
            if k not in self.frequent_itemsets:
                continue
                
            for itemset, itemset_support in self.frequent_itemsets[k].items():
                # Generate all non-empty proper subsets
                items = list(itemset)
                for i in range(1, len(items)):
                    for antecedent_items in combinations(items, i):
                        antecedent = frozenset(antecedent_items)
                        consequent = itemset - antecedent
                        
                        # Calculate confidence
                        antecedent_support = self.get_itemset_support(antecedent)
                        if antecedent_support > 0:
                            confidence = itemset_support / antecedent_support
                            
                            if confidence >= self.min_confidence:
                                lift = confidence / self.get_itemset_support(consequent)
                                
                                rule = {
                                    'antecedent': set(antecedent),
                                    'consequent': set(consequent),
                                    'support': itemset_support,
                                    'confidence': confidence,
                                    'lift': lift
                                }
                                self.association_rules.append(rule)
        
        # Sort by confidence
        self.association_rules.sort(key=lambda x: x['confidence'], reverse=True)
        print(f"Generated {len(self.association_rules)} association rules")
        
        return self.association_rules
    
    def get_itemset_support(self, itemset):
        """Get support for an itemset"""
        for k, itemsets in self.frequent_itemsets.items():
            if itemset in itemsets:
                return itemsets[itemset]
        return 0
    
    def mine_disease_specific_rules(self, df):
        """Mine association rules specific to each disease"""
        print("\nMining disease-specific symptom patterns...")
        
        diseases = df['Disease'].unique()
        for disease in diseases:
            disease_data = df[df['Disease'] == disease]
            transactions = self.get_transactions(disease_data)
            
            if len(transactions) < 3:  # Skip diseases with too few samples
                continue
            
            # Mine patterns for this disease
            miner = AprioriMiner(min_support=0.3, min_confidence=0.6)
            miner.mine_frequent_itemsets(transactions, max_length=3)
            
            # Store top patterns
            disease_patterns = []
            for k in sorted(miner.frequent_itemsets.keys(), reverse=True):
                for itemset, support in sorted(miner.frequent_itemsets[k].items(), 
                                              key=lambda x: x[1], reverse=True)[:5]:
                    disease_patterns.append({
                        'symptoms': list(itemset),
                        'support': support,
                        'size': len(itemset)
                    })
            
            if disease_patterns:
                self.disease_symptom_rules[disease] = disease_patterns
        
        print(f"Found patterns for {len(self.disease_symptom_rules)} diseases")
        return self.disease_symptom_rules
    
    def get_symptom_suggestions(self, selected_symptoms, top_n=3):
        """Get symptom suggestions based on association rules"""
        selected_set = set(selected_symptoms)
        suggestions = []
        
        for rule in self.association_rules:
            # If selected symptoms contain the antecedent
            if rule['antecedent'].issubset(selected_set):
                # Suggest symptoms in consequent that aren't selected
                new_symptoms = rule['consequent'] - selected_set
                if new_symptoms:
                    for symptom in new_symptoms:
                        suggestions.append({
                            'symptom': symptom,
                            'confidence': rule['confidence'],
                            'based_on': list(rule['antecedent'])
                        })
        
        # Sort by confidence and deduplicate
        seen = set()
        unique_suggestions = []
        for sugg in sorted(suggestions, key=lambda x: x['confidence'], reverse=True):
            if sugg['symptom'] not in seen:
                seen.add(sugg['symptom'])
                unique_suggestions.append(sugg)
        
        return unique_suggestions[:top_n]
    
    def get_disease_match_score(self, selected_symptoms, disease):
        """Calculate how well selected symptoms match a disease's patterns"""
        if disease not in self.disease_symptom_rules:
            return 0.0
        
        selected_set = set(selected_symptoms)
        max_score = 0.0
        
        for pattern in self.disease_symptom_rules[disease]:
            pattern_symptoms = set(pattern['symptoms'])
            # Calculate Jaccard similarity
            intersection = len(selected_set & pattern_symptoms)
            union = len(selected_set | pattern_symptoms)
            if union > 0:
                similarity = intersection / union
                weighted_score = similarity * pattern['support']
                max_score = max(max_score, weighted_score)
        
        return max_score
    
    def save_rules(self, filepath='models/apriori_rules.json'):
        """Save mined rules to file"""
        data = {
            'association_rules': [
                {
                    'antecedent': list(rule['antecedent']),
                    'consequent': list(rule['consequent']),
                    'support': float(rule['support']),
                    'confidence': float(rule['confidence']),
                    'lift': float(rule['lift'])
                }
                for rule in self.association_rules
            ],
            'disease_patterns': {
                disease: patterns
                for disease, patterns in self.disease_symptom_rules.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nSaved rules to {filepath}")
    
    def load_rules(self, filepath='models/apriori_rules.json'):
        """Load previously mined rules"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.association_rules = [
            {
                'antecedent': set(rule['antecedent']),
                'consequent': set(rule['consequent']),
                'support': rule['support'],
                'confidence': rule['confidence'],
                'lift': rule['lift']
            }
            for rule in data['association_rules']
        ]
        
        self.disease_symptom_rules = data['disease_patterns']
        print(f"Loaded {len(self.association_rules)} association rules")
        print(f"Loaded patterns for {len(self.disease_symptom_rules)} diseases")


def main():
    """Mine association rules from disease dataset"""
    print("="*60)
    print("APRIORI ASSOCIATION RULE MINING FOR SYMPTOMS")
    print("="*60)
    
    # Load dataset
    df = pd.read_csv('dataset_cleaned.csv')
    print(f"\nLoaded {len(df)} disease cases")
    print(f"Unique diseases: {df['Disease'].nunique()}")
    
    # Initialize miner
    miner = AprioriMiner(min_support=0.05, min_confidence=0.6)
    
    # Get transactions
    transactions = miner.get_transactions(df)
    print(f"Total transactions: {len(transactions)}")
    
    # Mine frequent itemsets
    frequent_itemsets = miner.mine_frequent_itemsets(transactions, max_length=4)
    
    # Print some examples
    print("\n--- Sample Frequent Itemsets ---")
    for k in sorted(frequent_itemsets.keys())[:3]:
        print(f"\n{k}-itemsets (top 5):")
        sorted_items = sorted(frequent_itemsets[k].items(), 
                            key=lambda x: x[1], reverse=True)[:5]
        for itemset, support in sorted_items:
            symptoms = ', '.join(sorted(itemset))
            print(f"  {{{symptoms}}} - support: {support:.3f}")
    
    # Generate association rules
    rules = miner.generate_association_rules()
    
    # Print top rules
    print("\n--- Top 10 Association Rules ---")
    for i, rule in enumerate(rules[:10], 1):
        ant = ', '.join(sorted(rule['antecedent']))
        cons = ', '.join(sorted(rule['consequent']))
        print(f"{i}. {{{ant}}} → {{{cons}}}")
        print(f"   Confidence: {rule['confidence']:.3f}, Support: {rule['support']:.3f}, Lift: {rule['lift']:.3f}")
    
    # Mine disease-specific patterns
    disease_rules = miner.mine_disease_specific_rules(df)
    
    # Print some disease patterns
    print("\n--- Sample Disease-Specific Patterns ---")
    for disease in list(disease_rules.keys())[:5]:
        print(f"\n{disease}:")
        for pattern in disease_rules[disease][:3]:
            symptoms = ', '.join(pattern['symptoms'])
            print(f"  {{{symptoms}}} - support: {pattern['support']:.3f}")
    
    # Save rules
    miner.save_rules()
    
    print("\n" + "="*60)
    print("APRIORI MINING COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
