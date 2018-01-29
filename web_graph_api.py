from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import json
import networkx as nx
from networkx.readwrite import json_graph
from textprocess import TextProcess
from dictionary import Dictionary
from localgridanalysis import LocalGridAnalysis
from graphvisualisation import GraphVisualisation
import os

#####
# App initialization
#####
app = Flask(__name__)
api = Api(app)
articles = json.load(open('data.json'))['articles']
GRAPH_DIR_PATH = "Graph/"

if not os.path.exists(GRAPH_DIR_PATH):
    os.makedirs(GRAPH_DIR_PATH)

def get_graph_path(name):
    name = "_".join(name.split())
    return "{}/{}".format(GRAPH_DIR_PATH, name)
    
def write_graph(graph, name):
    if graph is None:
        return
        
    path = get_graph_path(name)
    
    if not os.path.exists(path):
        nx.write_weighted_edgelist(graph, path, encoding="utf-8")
    
def get_graph(article):
    path = get_graph_path(article["name"])
    
    if os.path.exists(path):
        return nx.read_weighted_edgelist(path, encoding="utf-8")
        
    ###
    # Text processing
    ###
    # Create instance of TextProcess class that fetches text from url and filters it
    tp = TextProcess(url=article["url"], filename=article["name"], content_selector_dict=article["content-selector"])
    
    # Get filtered senteces in list
    filtered_sentences = tp.get_filtered_sentences()
    
    print("Got filtered sentences.")
    
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
    
    print("Got dictionary.")
    
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
    
    print("Set graph.")
    
    write_graph(graph, article["name"])
    
    return graph
    
class GraphResource(Resource):
    
    def get(self, article_id):
        print(request.args)
        print("article_id {}".format(article_id))
        if article_id < 1 or article_id > 4:
            abort(404, message = "Invalid text ID.")
       
        main_article = None
   
        for article in articles:
            if article['id'] == article_id:
                main_article = article
                break
   
        graph = get_graph(main_article)
        return json_graph.node_link_data(graph)
       
        
#####
# Resources
#####
api.add_resource(GraphResource, "/api/graph/<int:article_id>")

#####
# App config
#####
if __name__ == '__main__':    
    app.run(host ='0.0.0.0', port = 3000, debug=True)