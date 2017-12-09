import networkx as nx
from textprocess import TextProcess
from dictionary import Dictionary
from localgridanalysis import LocalGridAnalysis
from graphvisualisation import GraphVisualisation
import os


MAIN_EXPORT_PATH = "./GraphExports"

articles = [
    { "url" : "http://pogledaj.to/art/magija-i-folklor-u-velegradu/",
      "name" : "Magija i folklor u velegradu",
      "dictionary_path" : "./Oznake vrsta rijeci/GRUPA1/14-oznake.txt",
      "content-selector" : { "class" : "main the-content"}},
    { "url" : "http://pogledaj.to/art/veliki-paket-zraka/",
      "name" : "Veliki paket zraka",
      "dictionary_path" : "./Oznake vrsta rijeci/GRUPA1/3-oznake.txt",
      "content-selector" : { "class" : "main the-content"}},        
    { "url" : "http://pogledaj.to/arhitektura/vukovar-ceka-svoju-atrakciju/",
      "name" : "Vukovar ceka svoju atrakciju",
      "dictionary_path" : "./Oznake vrsta rijeci/GRUPA1/2-oznake.txt",
      "content-selector" : { "class" : "main the-content"}},
    { "url" : "http://pogledaj.to/art/zivot-je-cupav-i-dlakav/",
      "name" : "Zivot je cupav i dlakav",
      "dictionary_path" : "./Oznake vrsta rijeci/GRUPA1/6-oznake.txt",
      "content-selector" : { "class" : "main the-content"}},]          

    
for article in articles:
    ###
    # Text processing
    ###
    # Create instance of TextProcess class that fetches text from url and filters it
    tp = TextProcess(url=article["url"], filename=article["name"], content_selector_dict=article["content-selector"])
    
    # Get filtered senteces in list
    filtered_sentences = tp.get_filtered_sentences()
    
    ###
    # Dictionary extraction
    ###
    # Create instance of Dictionary class comparses filtered sentences with those in 
    # dictionary and creates node and edge list
    wt = Dictionary(dictionary_path=article["dictionary_path"])
    
    # Sets node nad edge list. First parameter is fitlered sentences, second is array
    # of wanted word types. Words that are not connected to other are set as node list
    # those that are connected are stored as edge list
    wt.set_words_as_node_and_egde_list(filtered_sentences, [Dictionary.NOUN])
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
    
    ###
    # Centralities calculation
    ###
    # Create instance of LocalGridAnalysis that contains methods for calculation centralities
    lga = LocalGridAnalysis(graph = graph)
    degree_centrality_nodes = lga.get_degree_centrality_nodes()
    betweenness_centrality_nodes = lga.get_betweenness_centrality_nodes()
    pagerank_nodes = lga.get_pagerank_nodes()
    
    print("---------- {} ---------".format(article["name"]))
    print("Degree centrality: {}".format(degree_centrality_nodes[0:5]))
    print("Betweenness centrality: {}".format(betweenness_centrality_nodes[0:5]))
    print("Pagerank centrality: {}".format(pagerank_nodes[0:5]))
    
    ###
    # Setting directories where plots and images for each article will be exported
    ###
    # Takes article name and replaces specases with underscores '_'
    concat_article_name = "_".join(article["name"].split())
    # Directory where visualised and gephi graph will be exported
    export_directories_path = "{}/{}/".format(MAIN_EXPORT_PATH, concat_article_name)
    
    # Create export directory if doesn't exist
    if not os.path.exists(export_directories_path):
        os.makedirs(export_directories_path)
    
    ###
    # Graph visualisation
    ###
    # Create instance of GraphVisualisation class and its constructor
    # takes graph and ande path where cisualised items will be stored
    gv = GraphVisualisation(graph = graph, save_dir_path = export_directories_path)    
    # Visualize degree centrality
    gv.visualize_graph_centrality(centrality_nodes = degree_centrality_nodes, window_title = article['name'], plot_title = 'Degree Centrality')
    # Visualize betweenness centrality
    gv.visualize_graph_centrality(centrality_nodes = betweenness_centrality_nodes, window_title = article['name'], plot_title = 'Betweenness Centrality')
    # Visualize pagerank
    gv.visualize_graph_centrality(centrality_nodes = pagerank_nodes, window_title = article['name'], plot_title = 'Pagerank')  
    
    ###
    # Gephi export
    ###
    nx.write_gexf(graph, "{}/{}.gexf".format(export_directories_path, concat_article_name))
    
