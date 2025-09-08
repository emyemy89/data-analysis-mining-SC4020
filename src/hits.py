###
# HITS will give two scores per node (hub and authority) 
# showing different roles in the  network
###

import json
import networkx as nx

# Load JSON dataset
with open('datasets/citation_network.json') as f:
    data = json.load(f)

# Create directed graph
G = nx.DiGraph()
for node in data['nodes']:
    G.add_node(node['id'], label=node.get('label'))
for edge in data['edges']:
    G.add_edge(edge['source'], edge['target'])

# Compute HITS scores
hubs, authorities = nx.hits(G, max_iter=100, normalized=True)

# Print results
print("Hub scores:", hubs)
print("Authority scores:", authorities)
