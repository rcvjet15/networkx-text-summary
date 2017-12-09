###
# This script creates figure for each article and in each figure subplot, image of centrality is displayed
###

import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Main path where all exports are stored
MAIN_EXPORT_PATH = "./GraphExports"

# articles dictionary array that contains name for each article
articles = [
    {"name" : "Magija i folklor u velegradu"},
    {"name" : "Veliki paket zraka",},
    {"name" : "Vukovar ceka svoju atrakciju"},
    {"name" : "Zivot je cupav i dlakav"},]

# Centralities that will be display in each figure
centralities= ["Degree Centrality", "Betweenness Centrality", "Pagerank", "KeywordsStudents"]

# Number of rows and columns on figure
rows = math.floor(len(centralities) / 2)
cols = math.ceil(len(centralities) / 2)

for article in articles:
    
    figure, axarr = plt.subplots(rows, cols, sharex = 'col', sharey = 'row')
    figure.canvas.set_window_title(article["name"])
    
    subdir_path = "{}/{}".format(MAIN_EXPORT_PATH, "_".join(article["name"].split()))
    col = 0
    row = 0
    for idx, centrality in enumerate(centralities):        
        img = mpimg.imread("{}/{}_gephi.png".format(subdir_path, centrality))
        
        subplot_ax = axarr[row, col]
        subplot_ax.imshow(img)
        subplot_ax.set_title(centrality)
        
        if col < cols - 1:
            col += 1  
        else:
            row += 1
            col = 0
               
        plt.setp(subplot_ax.get_yticklabels(), visible=False)
        plt.setp(subplot_ax.get_xticklabels(), visible=False)
    
    figure.tight_layout()
    figure.savefig("{}/Subplots.png".format(subdir_path))    

plt.show()
