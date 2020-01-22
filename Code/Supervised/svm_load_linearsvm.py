import networkx as nx
from sklearn import svm
from sklearn.svm import LinearSVR
import pickle
import numpy as np

st1 = "edges.txt"
st2 = "ques_pairs_with_groundtruth.txt"
st3 = "rank_nodes_pagerank_without_weight.txt"
st4 = "inverse_rankings.txt"

nooffeatures = 9
directed_graph = nx.DiGraph()
undirected_graph = nx.DiGraph()
pagerank_dict = {}
leader_fol_dict = {}

graph_file = open(st1)
for line in graph_file:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    directed_graph.add_edge(v1, v2)
    undirected_graph.add_edge(v1, v2)
    undirected_graph.add_edge(v2, v1)
    
tested_graph_file = open(st2)
for line in tested_graph_file:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    undirected_graph.add_edge(v1, v2)
    undirected_graph.add_edge(v2, v1)

pagerank_file = open(st3)
for line in pagerank_file:
    v1 = int(line.split(" ")[0])
    pagerankk = float(line.split(" ")[1])
    pagerank_dict[ v1 ] = pagerankk
    
leader_follower_file = open(st4)
for line in leader_follower_file:
    v1 = int(line.split(" ")[0])
    leader_fol_score = float(line.split(" ")[1])
    leader_fol_dict[ v1 ] = leader_fol_score

clf = LinearSVR(random_state=0)
with open("LinearSVR.dump", "rb") as fp:    # Unpickling
	clf = pickle.load(fp)

with open("node_centrality.dump", "rb") as fp:   # Unpickling
	bw_centrality = pickle.load(fp)
    
with open("edge_centrality.dump", "rb") as fp:   # Unpickling
	ew_centrality = pickle.load(fp)
    
popo = 0
def getfeatures(vert1, vert2):
    vect = []
    vect.append( bw_centrality.get(vert1) )
    vect.append( bw_centrality.get(vert2) )
    vect.append( ew_centrality.get( (vert1, vert2) ) ) 
    vect.append( pagerank_dict.get(vert1) )
    vect.append( pagerank_dict.get(vert2) )
    vect.append( undirected_graph.degree(vert1) )
    vect.append( undirected_graph.degree(vert2) )
    vect.append( leader_fol_dict.get(vert1) )
    vect.append( leader_fol_dict.get(vert2) ) 
    global popo
    popo += 1
    
    if(popo<=20):
       print bw_centrality.get(vert1), bw_centrality.get(vert2), ew_centrality.get( (vert1, vert2) ), pagerank_dict.get(vert1), pagerank_dict.get(vert2), undirected_graph.degree(vert1), undirected_graph.degree(vert2), leader_fol_dict.get(vert1), leader_fol_dict.get(vert2)
    
    return vect
    
correct = 0
noofval = 0
rejected = 0
tested_graph_file2 = open(st2)
for line in tested_graph_file2:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    
    img = getfeatures(v1, v2)
    try:
      labell = clf.predict([img])
      if( labell==1 ):
         correct += 1
    except Exception: 
	 rejected += 1
         pass

    noofval += 1
       
print correct, noofval, rejected
print (float(correct)/noofval)
