import networkx as nx
from operator import itemgetter

class LocalGridAnalysis:
        
    def __init__(self, graph):
        self._graph = graph
        
    def get_degree_centrality_top_nodes(self, reverseOrder = True):
        nodes_degree_centrality = nx.degree_centrality(self._graph)
        return sorted(nodes_degree_centrality.items(), reverse=reverseOrder, key=itemgetter(1))
        
    def get_betweenness_centrality_top_nodes(self, reverseOrder = True):
        betwenness_centrality = nx.betweenness_centrality(self._graph)        
        return sorted(betwenness_centrality.items(), reverse=reverseOrder, key=itemgetter(1))
        
    def get_pagerank_top_nodes(self, reverseOrder = True):
        pagerank = nx.pagerank(self._graph)
        return sorted(pagerank.items(), reverse=reverseOrder, key=itemgetter(1))