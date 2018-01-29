from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import json
import networkx as nx
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


class GraphApi(Resource):
    
    def get(self, text_id):
        
#####
# Resources
#####
api.add_resource(GraphApi, "/graph-api")

#####
# App config
#####
if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3000)