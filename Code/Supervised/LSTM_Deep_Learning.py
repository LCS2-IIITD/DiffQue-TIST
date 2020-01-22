from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers.core import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
import networkx as nx
import pickle
import numpy as np

st1 = "edges.txt"
st2 = "ques_pairs_with_groundtruth.txt"
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
    
time_diff_acc = open(st5)
for line in time_diff_acc:
    v1 = int(line.split(" ")[0])
    v2 = float(line.split(" ")[1])
    time_diff_of_accepted[ v1 ] = v2

answer_count = open(st6)
maxx = 0
for line in answer_count:
    v2 = int(line.split(" ")[1])
    maxx = max(maxx, v2)
    
answer_countt_2 = open(st6)
for line in answer_countt_2:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    flfl = float(v2)/maxx
    accepted_answer_id[ v1 ] = flfl

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
    vect.append( pagerank_dict.get(vert1) )
    vect.append( pagerank_dict.get(vert2) )
    vect.append( undirected_graph.degree(vert1) )
    vect.append( undirected_graph.degree(vert2) )
    vect.append( check2(vert1) )
    vect.append( check2(vert2) )
    vect.append( check3(vert1) )
    vect.append( check3(vert2) )
    vect.append( leader_fol_dict.get(vert1) )
    vect.append( leader_fol_dict.get(vert2) )
    
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
        
        train_x.append( img )
        train_y.append( lab )
        
    print('hi2')
    for ed in directed_graph.edges():
        v1 = ed[1]
        v2 = ed[0]
        lab = 0
        
        img = getfeatures(v1, v2)
  	
        train_x.append( img )
        train_y.append( lab )

    print('hi3')
    test_y = []
    test_x = []
    tested_graph_file2 = open(st2)
    for line in tested_graph_file2:
        v1 = int(line.split(" ")[0])
        v2 = int(line.split(" ")[1])
        v3 = int(line.split(" ")[2])
        
        img = getfeatures(v1, v2)
        if None not in img:
            test_x.append(img)
            if( v2==v3 ):
              test_y.append(1)
            else:
              test_y.append(0)  
     
    return train_x, train_y, test_x, test_y
                    
train_x, train_y, test_x, test_y = preprocess()

trainvector = np.reshape( train_x, (len(train_x), 1, nooffeatures) )
trainlabel = np.reshape( train_y, (len(train_y), 1) )
testvector = np.reshape( test_x, (len(test_x), 1, nooffeatures) )
testlabel = np.reshape( test_y, (len(test_y), 1) )

print('Defining')
model = Sequential()
model.add(LSTM(nooffeatures, input_shape=(1, nooffeatures)))
#model.add(Dropout(0.5))
#model.add(Dense(nooffeatures, activation='softmax'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])
print('Training')
model.fit(trainvector, trainlabel, epochs = 50, batch_size=64)

# Final evaluation of the model
scores = model.evaluate(testvector, testlabel, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
