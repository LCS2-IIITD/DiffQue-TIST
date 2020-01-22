import networkx as nx
import pickle
from sklearn.svm import LinearSVR
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

st1 = "edges.txt"
st2 = "merger2.txt"
st3 = "rank_nodes_pagerank_without_weight.txt"
st4 = "inverse_rankings.txt"
st5 = "time_diff.txt"
st6 = "ans_count.txt"

nooffeatures = 10
directed_graph = nx.DiGraph()
undirected_graph = nx.DiGraph()
pagerank_dict = {}
leader_fol_dict = {}
bw_centrality = {}
accepted_answer_id = {}
time_diff_of_accepted = {}
degree = {}

graph_file = open(st1)
for line in graph_file:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    directed_graph.add_edge(v1, v2)
    
    if( v1 in degree ):
        degree[v1] += 1
    else:
        degree[v1] = 1
    if( v2 in degree ):
        degree[v2] += 1
    else:
        degree[v2] = 1

pagerank_file = open(st3)
for line in pagerank_file:
    v1 = int(line.split(" ")[0])
    pagerankk = float(line.split(" ")[1])
    #pagerankk = "%.8f" % ( float(line.split(" ")[1]) )
    pagerank_dict[ v1 ] = pagerankk

max1 = 0
leader_follower_file = open(st4)
for line in leader_follower_file:
    v1 = int(line.split(" ")[0])
    leader_fol_score = float(line.split(" ")[1])
    max1 = max(max1, leader_fol_score)
    
leader_follower_file = open(st4)
for line in leader_follower_file:
    v1 = int(line.split(" ")[0])
    leader_fol_score = float(line.split(" ")[1])
    leader_fol_dict[ v1 ] = float(leader_fol_score)/max1

max1 = 0
time_diff_acc = open(st5)
for line in time_diff_acc:
    v1 = int(line.split(" ")[0])
    v2 = float(line.split(" ")[1])
    max1 = max(max1, v2)
    
time_diff_acc = open(st5)
for line in time_diff_acc:
    v1 = int(line.split(" ")[0])
    v2 = float(line.split(" ")[1])
    time_diff_of_accepted[ v1 ] = float(v2)/max1

max1 = 0
answer_count = open(st6)
for line in answer_count:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    max1 = max(max1, v2)
   
answer_count = open(st6)
for line in answer_count:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    accepted_answer_id[ v1 ] = float(v2)/max1

def check2( vert ):
    if( vert in accepted_answer_id ):
        return accepted_answer_id[vert]
    return 0

def check3( vert ):
    if( vert in time_diff_of_accepted ):
        return time_diff_of_accepted[vert]
    return 1
    
def getfeatures(vert1, vert2):
    vect = []
    #vect.append( bw_centrality.get(vert1) )
    #vect.append( bw_centrality.get(vert2) )

    if( vert1 in leader_fol_dict ):       
       vect.append( leader_fol_dict.get(vert1) )
    else:
       vect.append(0)    
    if( vert2 in leader_fol_dict ):       
       vect.append( leader_fol_dict.get(vert2) )
    else:
       vect.append(0)     
    
    if( vert1 in pagerank_dict ):       
       vect.append( pagerank_dict.get(vert1) )
    else:
       vect.append(0)    
    if( vert2 in pagerank_dict ):       
       vect.append( pagerank_dict.get(vert2) )
    else:
       vect.append(0)    
    
    if( vert1 is degree ):       
       vect.append( degree[vert1] )
    else:
       vect.append(0)    
    if( vert2 is degree ):       
       vect.append( degree[vert2] )
    else:
        vect.append(0)   
    
    vect.append( check2(vert1) )
    vect.append( check2(vert2) )
    
    vect.append( check3(vert1) )
    vect.append( check3(vert2) )
        
    return vect
    
def preprocess():
    train_x = []
    train_y = []

    print('hi')
    for ed in directed_graph.edges():
        v1 = ed[0]
        v2 = ed[1]
        lab = 1

        img = getfeatures(v1, v2)
        if( None not in img ):
            train_x.append( img )
            train_y.append( lab )

    print('hi2')
    for ed in directed_graph.edges():
        v1 = ed[1]
        v2 = ed[0]
        lab = 0
        
        img = getfeatures(v1, v2)
  	
        if( None not in img ):
            train_x.append( img )
            train_y.append( lab )
     
    return train_x, train_y   
                    
train_x, train_y = preprocess()
        
trainvector = np.reshape( train_x, (len(train_x), nooffeatures) )
trainlabel = np.reshape( train_y, (len(train_y), 1) )

print('Defining')
clf2 = svm.SVC(kernel='linear', C = 1.0)
with open("SVM_Classifier.dump", "rb") as fp:    # Unpickling
	clf2 = pickle.load(fp)
#clf2 = KNeighborsClassifier(n_neighbors=12) 
#clf2 = GaussianNB()
#clf2 = svm.SVC(kernel='rbf')   # 0.554045444893
#clf2 = DecisionTreeClassifier(criterion = "gini")
#clf2 = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,15,), random_state=1) # 0.554045444893
#print('Training')
#clf2.fit(trainvector, trainlabel)

print('Checking')
correct = 0
incorrect = 0
noofval = 0
rejected = 0
t1 = []
t2 = []
tested_graph_file2 = open(st2)
for line in tested_graph_file2:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    v3 = int(line.split(" ")[2])
        
    img = getfeatures(v1, v2)
    try:
        labell = clf2.predict([img])
        if( v3==v2 ):
            t1.append(1)
            
            if( labell==1 ):
              t2.append(1)
              correct += 1
            else:
              t2.append(0)
              incorrect += 1
              print(v1, " ", v2, " ", v3)
        else:
            t1.append(0)
            
            if( labell==0 ):
              t2.append(0)
              correct += 1
            else:
              t2.append(1)
              incorrect += 1
              print(v1, " ", v2, " ", v3)
    except Exception: 
        rejected += 1
        pass

    noofval += 1
       
print( correct, noofval, rejected, incorrect )
print( (float(correct)/noofval) )

print( f1_score(t1, t2, average='macro') )
with open("SVM_Classifier.dump", "wb") as fp1:   #Pickling
	pickle.dump(clf2, fp1)
