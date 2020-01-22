import networkx as nx
import pickle
from sklearn import svm
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
    
maxv1 = 0.0
leader_follower_file = open(st4)
for line in leader_follower_file:
    maxv1 = max( maxv1, float(line.split(" ")[1]) )

leader_follower_file = open(st4)
for line in leader_follower_file:
    v1 = int(line.split(" ")[0])
    leader_fol_score = float(line.split(" ")[1])
    leader_fol_dict[ v1 ] = leader_fol_score/maxv1

print "Node centrality"
bw_centrality = nx.betweenness_centrality(directed_graph, k = 10000, normalized=True)
with open("node_centrality.dump", "wb") as fp1:   #Pickling
	pickle.dump(bw_centrality, fp1)

print "Edge centrality"
ew_centrality = nx.edge_betweenness_centrality(undirected_graph, normalized=True)
with open("edge_centrality.dump", "wb") as fp1:   #Pickling
	pickle.dump(ew_centrality, fp1)
 
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
    
    return vect
    
def preprocess():
    train_x = []
    train_y = []

    popo2 = 0	
    print('hi')
    for ed in directed_graph.edges():
        v1 = ed[0]
        v2 = ed[1]
        lab = 1
        popo2 += 1
	
        img = getfeatures(v1, v2)
        if( popo2<=10 ): 
    		print v1, v2
    		print img
       
        train_x.append( img )
        train_y.append( lab )
        
    popo2 = 0
    print('hi2')
    for ed in directed_graph.edges():
        v1 = ed[1]
        v2 = ed[0]
        lab = 0
        popo2 += 1
                                      
        img = getfeatures(v1, v2)
        if( popo2<=10 ):
    		print v1, v2
    		print img
		
        train_x.append( img )
        train_y.append( lab )
     
    return train_x, train_y   

train_x, train_y = preprocess()
        
trainvector = np.reshape( train_x, (len(train_x), nooffeatures) )
trainlabel = np.reshape( train_y, (len(train_y), 1) )
with open("Trainvector.dump", "wb") as fp1:   #Pickling
	pickle.dump(trainvector, fp1)
with open("Trainlabel.dump", "wb") as fp1:   #Pickling
	pickle.dump(trainlabel, fp1)

print('Defining')
clf = svm.SVC(kernel='rbf', C=1)
print('Training')
clf.fit(trainvector, trainlabel.ravel())

with open("KernelRBFc.dump", "wb") as fp1:   #Pickling
	pickle.dump(clf, fp1)
    
rejected = 0    
correct = 0
noofval = 0
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
