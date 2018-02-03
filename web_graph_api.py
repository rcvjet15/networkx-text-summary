from flask import Flask, request
from flask_restful import abort
from flask_cors import CORS
import json
import networkx as nx
import graph_lib as glib
import os
from dictionary import Dictionary

#####
# App initialization
#####
app = Flask(__name__)
CORS(app)
articles = json.load(open('data.json'))['articles']
GRAPH_DIR_PATH = "Graph/"

if not os.path.exists(GRAPH_DIR_PATH):
    os.makedirs(GRAPH_DIR_PATH)

def get_graph_path(name):
    name = "_".join(name.split())
    return "{}/{}".format(GRAPH_DIR_PATH, name)
    
def save_graph(graph, name):
    if graph is None:
        return
        
    path = get_graph_path(name)
    
    if not os.path.exists(path):
        nx.write_weighted_edgelist(graph, path, encoding="utf-8")
    
def load_graph(article, dictionary_types = [Dictionary.NOUN], fetch_from_url = False):
    if not fetch_from_url:
        path = get_graph_path(article["name"])
    
        if os.path.exists(path):
            return nx.read_weighted_edgelist(path, encoding="utf-8")        
    
    graph = glib.get_graph(article, dictionary_types)
    
    save_graph(graph, article["name"])
    
    return graph

def load_article(article_id):
    main_article = None
    
    for article in articles:
        if article['id'] == article_id:
            main_article = article
            break
        
    if article is None:
        abort(404, message = "Invalid article ID.")
            
    return main_article

#####
# Routes
#####
@app.route("/api/graphs")
def get_graph():
    
    article_id = int(request.args.get("article_id"))
    dict_types = list(request.args.getlist("dictionary_types"))
    
    print("Request args: {}".format([article_id, dict_types]))
    
    article = load_article(article_id)    
    graph = load_graph(article, dict_types, fetch_from_url = True)
    graph_data = glib.get_sigma_graph(graph)            
    
    # return json.dumps({"nodes": graph.nodes(), "edges": graph.edges()})
    return json.dumps(graph_data)
        
@app.route("/api/article/<int:article_id>")
def get_article(article_id):
    article = load_article(article_id)
    
    article["text"] = glib.get_filtered_sentences(article)
    return json.dumps(article)
        

#####
# App config
#####
if __name__ == '__main__':    
    app.run(host ='0.0.0.0', port = 3000, debug=True)