###
# PageRank will give one score per node (overall importance)
###

import networkx as nx

# Create or load a directed graph
G = nx.DiGraph()
G.add_edges_from([(1,2), (2,3), (3,1), (3,4)])

# Compute PageRank
pagerank_scores = nx.pagerank(G, alpha=0.85)

print(pagerank_scores)

