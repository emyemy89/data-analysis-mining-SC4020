import networkx as nx

# Load undirected graph from the edge list
G = nx.read_edgelist("../datasets/facebook_combined.txt", create_using=nx.Graph(), nodetype=int)

# HITS requires a directed graph
G = G.to_directed()

# Compute HITS scores
hubs, authorities = nx.hits(G, max_iter=100, normalized=True)

# Print top 10 hubs
print("Top Hub Scores:")
top_hubs = sorted(hubs.items(), key=lambda x: x[1], reverse=True)[:10]
for node, score in top_hubs:
    print(f"Node {node}: Hub Score = {score:.5f}")

# Print top 10 authorities
print("\nTop Authority Scores:")
top_auths = sorted(authorities.items(), key=lambda x: x[1], reverse=True)[:10]
for node, score in top_auths:
    print(f"Node {node}: Authority Score = {score:.5f}")
