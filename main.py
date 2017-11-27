from textprocess import TextProcess

articles = [
        { "url" : "http://pogledaj.to/art/veliki-paket-zraka/",
          "name" : "Veliki paket zraka",
          "word_marks_path" : "./Oznake vrsta rijeci/3-oznake.txt" },
        { "url" : "http://pogledaj.to/art/pogreske-su-pozeljne/",
          "name" : "Pogreske su pozeljne",
          "word_marks_path" : "./Oznake vrsta rijeci/3-oznake.txt" },
        { "url" : "http://pogledaj.to/arhitektura/vukovar-ceka-svoju-atrakciju/",
          "name" : "Vukovar ceka svoju atrakciju",
          "word_marks_path" : "./Oznake vrsta rijeci/2-oznake.txt",
          "content-selector" : { "class" : "main the-content"}},
        { "url" : "http://pogledaj.to/art/zivot-je-cupav-i-dlakav/",
          "name" : "Zivot je cupav i dlakav",
          "word_marks_path" : "./Oznake vrsta rijeci/6-oznake.txt",
          "content-selector" : { "class" : "main the-content"}}]

tp = TextProcess(url=articles[2]["url"], filename=articles[2]["name"], content_selector_dict=articles[2]["content-selector"])

for sentence in tp.start_process():
    print("-----------------------------------------------------\n{}".format(sentence))