from textprocess import TextProcess
from wordtypes import WordTypes

articles = [
        { "url" : "http://pogledaj.to/art/veliki-paket-zraka/",
          "name" : "Veliki paket zraka",
          "word_marks_path" : "./Oznake vrsta rijeci/GRUPA1/3-oznake.txt",
          "content-selector" : { "class" : "main the-content"}},
        { "url" : "http://pogledaj.to/art/pogreske-su-pozeljne/",
          "name" : "Pogreske su pozeljne",
          "word_marks_path" : "./Oznake vrsta rijeci/GRUPA1/3-oznake.txt",
          "content-selector" : { "class" : "main the-content"}},
        { "url" : "http://pogledaj.to/arhitektura/vukovar-ceka-svoju-atrakciju/",
          "name" : "Vukovar ceka svoju atrakciju",
          "word_marks_path" : "./Oznake vrsta rijeci/GRUPA1/2-oznake.txt",
          "content-selector" : { "class" : "main the-content"}},
        { "url" : "http://pogledaj.to/art/zivot-je-cupav-i-dlakav/",
          "name" : "Zivot je cupav i dlakav",
          "word_marks_path" : "./Oznake vrsta rijeci/GRUPA1/6-oznake.txt",
          "content-selector" : { "class" : "main the-content"}}]

tp = TextProcess(url=articles[2]["url"], filename=articles[2]["name"], content_selector_dict=articles[2]["content-selector"])

# Get filtered senteces in list
filtered_sentences = tp.get_filtered_sentences()

wt = WordTypes(word_marks_path=articles[2]["word_marks_path"])

wt.get_marked_words_list(filtered_sentences, [WordTypes.NOUN])



#for sentence in filtered_sentences:
#    print("-----------------------------------------------------\n{}".format(sentence))