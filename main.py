from textprocess import TextProcess
from dictionary import Dictionary
import networkx as nx

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

article = articles[0]

tp = TextProcess(url=article["url"], filename=article["name"], content_selector_dict=article["content-selector"])

# Get filtered senteces in list
filtered_sentences = tp.get_filtered_sentences()

wt = Dictionary(dictionary_path=article["word_marks_path"])

wt.set_words_as_node_and_egde_list(filtered_sentences, [Dictionary.NOUN])
wt.set_edge_list_as_weighted_edges()

g = nx.Graph()
g.add_nodes_from(wt.node_list)
g.add_weighted_edges_from(wt.edge_list)
nx.draw(g, with_labels = True)

#for sentence in filtered_sentences:
#    print("-----------------------------------------------------\n{}".format(sentence))