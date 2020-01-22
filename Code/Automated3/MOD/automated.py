import os
import sys
from os import system
import shutil

filenames = ["edges_chinese_old.txt", "edges_msr_old.txt"]
def RemoveNewLine(oldfilename, newfilename):
	f = open(oldfilename)
	lines = f.readlines()
	f.close()
	lines[-1] = lines[-1].rstrip()
	f = open(newfilename, 'w')
	f.writelines(lines)
	f.close()

for filename in filenames:
 
    try:
        os.remove("page_rank/" + filename)
    except OSError:
        pass
    try:
        os.remove("page_rank/" + "edges.txt")
    except OSError:
        pass
    try:
        os.remove("page_rank/" + "rank_nodes_pagerank_without_weight.txt")
    except OSError:
        pass
   
    RemoveNewLine(filename, filename)
    print "Processing NPM"
    system("cp " + filename + " page_rank/")
    system("mv page_rank/" + filename + " page_rank/edges.txt")
    system("cd page_rank && npm start")
    '''
    print "Link Prediction"
    system("cp " + filename + " link_prediction/")
    system("mv link_prediction/" + filename + " link_prediction/edges.txt")
    system("python link_prediction/recursive_subgraph.py")
    
    print "Final Model"
    system("cp " + filename + " ns2/")
    system("cp " + "link_prediction/inverse_rankings.txt" + " ns2/")
    system("cp " + "page_rank/rank_nodes_pagerank_without_weight.txt" + " ns2/")
    system("mv ns2/" + filename + " ns2/edges.txt")
    system("python ns2/Decision_Tree.py")
    '''