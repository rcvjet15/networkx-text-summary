import networkx as nx
from textprocess import TextProcess
from dictionary import Dictionary
from localgridanalysis import LocalGridAnalysis
from graphvisualisation import GraphVisualisation
import os

articles = [
        { "url" : "http://pogledaj.to/art/veliki-paket-zraka/",
          "name" : "Veliki paket zraka",
          "word_marks_path" : "./Oznake vrsta rijeci/GRUPA1/3-oznake.txt",
          "content-selector" : { "class" : "main the-content"}},
        { "url" : "http://pogledaj.to/art/magija-i-folklor-u-velegradu/",
          "name" : "Magija i folklor u velegradu",
          "word_marks_path" : "./Oznake vrsta rijeci/GRUPA1/14-oznake.txt",
          "content-selector" : { "class" : "main the-content"}},
        { "url" : "http://pogledaj.to/arhitektura/vukovar-ceka-svoju-atrakciju/",
          "name" : "Vukovar ceka svoju atrakciju",
          "word_marks_path" : "./Oznake vrsta rijeci/GRUPA1/2-oznake.txt",
          "content-selector" : { "class" : "main the-content"}},
        { "url" : "http://pogledaj.to/art/zivot-je-cupav-i-dlakav/",
          "name" : "Zivot je cupav i dlakav",
          "word_marks_path" : "./Oznake vrsta rijeci/GRUPA1/6-oznake.txt",
          "content-selector" : { "class" : "main the-content"}}]

for article in articles[0:1]:
    tp = TextProcess(url=article["url"], filename=article["name"], content_selector_dict=article["content-selector"])
    
    # Get filtered senteces in list
    filtered_sentences = tp.get_filtered_sentences()
    
    wt = Dictionary(dictionary_path=article["word_marks_path"])
    
    wt.set_words_as_node_and_egde_list(filtered_sentences, [Dictionary.NOUN])
    wt.set_edge_list_as_weighted_edges()
    
    g = nx.DiGraph()
    g.add_nodes_from(wt.node_list)
    g.add_weighted_edges_from(wt.edge_list)
    
    lga = LocalGridAnalysis(graph = g)
    
    concat_article_name = "_".join(article["name"].split())
    export_directories_path = "./GraphExports/{}/".format(concat_article_name)
    
    if not os.path.exists(export_directories_path):
        os.makedirs(export_directories_path)
        
    gv = GraphVisualisation(graph = g, save_dir_path = export_directories_path)    
    gv.visualize_graph_centrality(centrality_nodes = lga.get_degree_centrality_nodes(), title = 'Degree Centrality')
    gv.visualize_graph_centrality(centrality_nodes = lga.get_betweenness_centrality_nodes(), title = 'Betweenness Centrality')
    gv.visualize_graph_centrality(centrality_nodes = lga.get_pagerank_nodes(), title = 'Pagerank')
    
    
#    
#    nx.write_gexf(g, "{}/{}.gexf".format(export_directories_path, concat_article_name))

#for sentence in filtered_sentences:
#    print("-----------------------------------------------------\n{}".format(sentence))