import networkx as nx
from operator import itemgetter

class LocalGridAnalysis:
        
    def __init__(self, graph):
        self._graph = graph
        
    def get_degree_centrality_top_nodes(self, top = 5):
        nodes_degree_centrality = nx.degree_centrality(self._graph)
        return sorted(nodes_degree_centrality.items(), reverse=True, key=itemgetter(1))[0:top]        
        
    def get_betweenness_centrality_top_nodes(self, top = 5):
        betwenness_centrality = nx.betweenness_centrality(self._graph)        
        return sorted(betwenness_centrality.items(), reverse=True, key=itemgetter(1))[0:top]
        
    def get_pagerank_top_nodes(self, top = 5):
        pagerank = nx.pagerank(self._graph)
        return sorted(pagerank.items(), reverse=True, key=itemgetter(1))[0:top]