from textprocess import TextProcess
from dictionary import Dictionary
from localgridanalysis import LocalGridAnalysis
from graphvisualisation import GraphVisualisation
import networkx as nx
from networkx.readwrite import json_graph

def get_filtered_sentences(article):
    ###
    # Text processing
    ###
    # Create instance of TextProcess class that fetches text from url and filters it
    tp = TextProcess(url=article["url"], filename=article["name"], content_selector_dict=article["content-selector"])
    
    # Get filtered senteces in list
    return tp.get_filtered_sentences()
    
def get_graph(article, dictionary_types = []):    
    ###
    # Dictionary extraction
    ###
    # Create instance of Dictionary class comparses filtered sentences with those in 
    # dictionary and creates node and edge list
    wt = Dictionary(dictionary_path=article["dictionary_path"])
    
    if (len(dictionary_types) == 0):
        dictionary_types = wt.all_types
        
    # Sets node nad edge list. First parameter is fitlered sentences, second is array
    # of wanted word types. Words that are not connected to other are set as node list
    # those that are connected are stored as edge list
    wt.set_words_as_node_and_egde_list(article["sentences"], dictionary_types)
    # Creates dictionary array that sets weight to amount of occurences of each pair
    wt.set_edge_list_as_weighted_edges()
           
    ###
    # Graph creation
    ###
    # Create directed graph
    graph = nx.DiGraph() 
    # Adds edges to graph. Passed parameter consists of dictionary where each element
    # is tuple that consists of: (node1, node2, weight)
    graph.add_weighted_edges_from(wt.edge_list)
    # Adds nodes list. Words that are not connected are stored as nodes list
    graph.add_nodes_from(wt.node_list)
    
    for node_value in graph.nodes():
        for nominative, original in wt.nominative_original_list:            
            if (node_value == nominative):                
                graph.node[node_value]['original'] = original
        for word, wordType in wt.words_types:
            if graph.node[node_value]['original'] == word:
                graph.node[node_value]['wordType'] = wordType
        
    return graph
    
def get_graph_edge_list(article):
    wt = Dictionary(dictionary_path=article["dictionary_path"])    
    wt.set_words_as_node_and_egde_list(article["sentences"], [Dictionary.NOUN])    
    wt.set_edge_list_as_weighted_edges()
    return wt.edge_list

def get_centrality_node_value(centrality_dict_arr, nodeKey):
    value = None
    for node in centrality_dict_arr:
        if node[0] == nodeKey:
            value = node[1]
            break
    
    return value
    
def get_sigma_graph(graph):
    
    graph_json = json_graph.node_link_data(graph)
    
    lga = LocalGridAnalysis(graph = graph)
    degree_centrality_nodes = lga.get_degree_centrality_nodes()
    betweenness_centrality_nodes = lga.get_betweenness_centrality_nodes()
    pagerank_nodes = lga.get_pagerank_nodes()
    
    # Add label key to node
    for node in graph_json["nodes"]:
        dCentrality = get_centrality_node_value(degree_centrality_nodes, node["id"])
        bCentrality = get_centrality_node_value(betweenness_centrality_nodes, node["id"])
        pagerank = get_centrality_node_value(pagerank_nodes, node["id"])
        
        node["label"] = node["id"]
        node["color"] = "#E1D804"
        node["degreeCentrality"] = dCentrality
        node["betweennessCentrality"] = bCentrality
        node["pagerank"] = pagerank
        node["size"] = dCentrality * 20
        
    graph_json["edges"] = []
    edge_count = 0
        
    for link in graph_json["links"]:
        source = link["source"]
        weight = link["weight"]
        target = link["target"]
        
        graph_json["edges"].append(
        {
            "id" : "e{}".format(edge_count),
            "source" : graph_json["nodes"][source]["id"],
            "target" : graph_json["nodes"][target]["id"],
            "size" : weight / 3
        })
        
        edge_count += 1
        
    graph_json["links"] = None
    
    return graph_json
    