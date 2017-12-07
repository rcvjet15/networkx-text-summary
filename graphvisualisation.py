import networkx as nx
import matplotlib as py
import matplotlib.pyplot as plt

class GraphVisualisation:
    
    DEFAULT_NODE_SIZE = 500
    DEFAULT_EDGE_WIDTH = 0.5
    LARGEST_NODE_SIZE = 1200
    LARGEST_LINEWIDTH = 3.0
    LARGEST_EDGE_WIDTH = 1
    
    def __init__(self, graph, save_dir_path):
        self._graph = graph
        self._save_dir_path = save_dir_path
        
    def visualize_graph_centrality(self, centrality_nodes, title, top = 5):
        plt.figure()
        plt.title(title)
        pos = nx.spring_layout(self._graph)
        
        # Draw smaller nodes and mark them in yellow color
        nx.draw(self._graph, pos, node_color='y', node_size=GraphVisualisation.DEFAULT_NODE_SIZE, width = GraphVisualisation.DEFAULT_EDGE_WIDTH, edge_color = 'y', with_labels=True, style='dotted')
        
        size = GraphVisualisation.LARGEST_NODE_SIZE
        linewidth = GraphVisualisation.LARGEST_LINEWIDTH
        edgewidth = GraphVisualisation.LARGEST_EDGE_WIDTH
        for node, value in centrality_nodes[0:top]:  
           
            nx.draw_networkx_nodes(self._graph, pos, nodelist=[node], node_size=size, node_color='r', with_labels=True, linewidths = linewidth)
            nx.draw_networkx_edges(self._graph, pos, width = edgewidth, edge_list=[(edge for edge in self._graph.edges() if edge[0] == node or edge[1] == node)], edge_color = 'r', arrows = True)
            size -= 100
            linewidth -= 0.5
            edgewidth -= 0.2
        
        plt.show()
        plt.savefig("{}/{}_matplot.png".format(self._save_dir_path, title))
       
#     fig, ax = plt.subplots(figsize=(15, 10))
#    plt.bar(degrees, counts, width = 0.7, color = 'b')
#    
#    plt.title("Degree Histogram")
#    plt.ylabel("Count")
#    plt.xlabel("Degree")
#    ax.set_xticks([d + 0.4 for d in degrees])
#    ax.set_xticklabels(degrees)