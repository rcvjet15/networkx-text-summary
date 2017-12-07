import networkx as nx
import matplotlib as py
import matplotlib.pyplot as plt

class GraphVisualisation:

    def __init__(self, graph):
        self._graph = graph
        
    def visualize_degree_centrality(self, degree_centrality_items, top = 5):
        plt.figure()
        plt.title("Degree centrality")
        pos = nx.spring_layout(self.graph)
        
        # Draw smaller nodes and mark them in yellow color
        nx.draw(self._graph, pos, node_color='y', node_size=80, with_labels=True)
        
        # Draw ego as large and red
        nx.draw_networkx_nodes(self._graph, pos, nodelist=[degree_centrality_items[0:top]], node_size=300, node_color='r', with_labels=True)
        
        plt.show()
        
#     fig, ax = plt.subplots(figsize=(15, 10))
#    plt.bar(degrees, counts, width = 0.7, color = 'b')
#    
#    plt.title("Degree Histogram")
#    plt.ylabel("Count")
#    plt.xlabel("Degree")
#    ax.set_xticks([d + 0.4 for d in degrees])
#    ax.set_xticklabels(degrees)