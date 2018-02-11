from flask import Flask, request
from flask_restful import abort
from flask_cors import CORS
import json
import networkx as nx
import graph_lib as glib
import os
from dictionary import Dictionary

#####
# Variables initialization
#####
app = Flask(__name__)
CORS(app)
GRAPH_DIR_PATH = "Graph/"
articles = json.load(open('data.json'))
USE_GRAPH_FILE = False # flag used to indicate if graph should be saved and read from file

#####
# App Methods
#####

def get_articles_sentences():
    should_save = False
    
    for article in articles: 
        # If article obj doesn't have sentences, fetch it and filter them
        if not "sentences" in article.keys() or not article["sentences"]:
            article["sentences"] = glib.get_filtered_sentences(article)  
            should_save = True
            
    if should_save:
        with open('data.json', 'w') as f:
            json.dump(articles, f, ensure_ascii=False)
        
def get_graph_path(name):
    name = "_".join(name.split())
    return "{}/{}".format(GRAPH_DIR_PATH, name)
    
def save_graph(graph, name):
    if graph is None or not USE_GRAPH_FILE:
        return
        
    path = get_graph_path(name)
    
    if not os.path.exists(path):
        nx.write_weighted_edgelist(graph, path, encoding="utf-8")
    
def load_graph(article, dictionary_types):
    
    if USE_GRAPH_FILE:
        path = get_graph_path(article["name"])
    
        if os.path.exists(path):
            return nx.read_weighted_edgelist(path, encoding="utf-8")        
    
    # dictionary_types = [Dictionary.NOUN, Dictionary.CONJUCTION]
    graph = glib.get_graph(article, dictionary_types)
    
    if USE_GRAPH_FILE:
        save_graph(graph, article["name"])
    
    return graph

def load_article(article_id):
    main_article = None
    
    for article in articles:            
        if article['id'] == article_id:
            main_article = article
            break
    
    if main_article is None:
        abort(404, message = "Invalid article ID.")
        
    return main_article

#####
# Routes
#####
@app.route("/api/all-graphs")
def get_all_graphs():
    all_graphs_data = []
    dict_types = []
    
    for article in articles:
        article = load_article(article["id"])    
        graph = load_graph(article, dict_types)    
        graph_data = glib.get_sigma_graph(graph)
        graph_data["articleId"] = article["id"]
        all_graphs_data.append(graph_data)
        
    return json.dumps(all_graphs_data)
    
@app.route("/api/graphs")
def get_graph():
    
    article_id = int(request.args.get("article_id"))
    dict_types_json = request.args.get("dictionary_types")
    
    dict_types = []
    
    if dict_types_json is not None:
        dict_types = [value for value in json.loads(dict_types_json).values()]
            
    article = load_article(article_id)    
    graph = load_graph(article, dict_types)    
    graph_data = glib.get_sigma_graph(graph)
    graph_data["articleId"] = article["id"]
    
    return json.dumps(graph_data)

@app.route("/api/articles")
def get_articles():        
    return json.dumps(articles)
      
@app.route("/api/article/<int:article_id>")
def get_article(article_id):
    article = load_article(article_id)
    
    article["sentences"] = glib.get_filtered_sentences(article)
    return json.dumps(article)
        
    
#####
# App config and startup
#####
if not os.path.exists(GRAPH_DIR_PATH):
    os.makedirs(GRAPH_DIR_PATH)
        
get_articles_sentences()

if __name__ == '__main__':        
    app.run(host ='0.0.0.0', port = 3000, debug=True)