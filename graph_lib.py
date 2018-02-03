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
    
def get_graph(article, dictionary_types):
    
    filtered_sentences = get_filtered_sentences(article)
    
    ###
    # Dictionary extraction
    ###
    # Create instance of Dictionary class comparses filtered sentences with those in 
    # dictionary and creates node and edge list
    wt = Dictionary(dictionary_path=article["dictionary_path"])
    
    # Sets node nad edge list. First parameter is fitlered sentences, second is array
    # of wanted word types. Words that are not connected to other are set as node list
    # those that are connected are stored as edge list
    wt.set_words_as_node_and_egde_list(filtered_sentences, dictionary_types)
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
    
    return graph
    
def get_graph_edge_list(article):
    filtered_sentences = get_filtered_sentences(article)
    
    wt = Dictionary(dictionary_path=article["dictionary_path"])    
    wt.set_words_as_node_and_egde_list(filtered_sentences, [Dictionary.NOUN])    
    wt.set_edge_list_as_weighted_edges()
    return wt.edge_list
    
def get_sigma_graph(graph):
    
    graph_json = json_graph.node_link_data(graph)
    
    # Add label key to node
    for node in graph_json["nodes"]:
        node["label"] = node["id"].title()
    
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
            # "size" : weight * 10,
            # "color" : "red"            
        })
        
        edge_count += 1
        
    graph_json["links"] = None
    
    return graph_json
    