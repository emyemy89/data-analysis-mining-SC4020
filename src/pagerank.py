import networkx as nx

# Load the undirected graph from the file
G = nx.read_edgelist("../datasets/facebook_combined.txt", create_using=nx.Graph(), nodetype=int)

# Convert to directed for PageRank (optional, PageRank works on both)
G = G.to_directed()

# Compute PageRank
pagerank_scores = nx.pagerank(G, alpha=0.85)

# Print top 10 nodes by PageRank score
top_nodes = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:10]
for node, score in top_nodes:
    print(f"Node {node}: PageRank = {score:.5f}")


