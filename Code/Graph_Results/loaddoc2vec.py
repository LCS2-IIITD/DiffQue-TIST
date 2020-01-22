import logging
import gensim, os
import xml.etree.cElementTree
from nltk.corpus import stopwords
from string import ascii_lowercase
from collections import namedtuple
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from sklearn import svm
import pickle
import networkx as nx

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

dictt = {}
corpora_documents = []
st1 = "edges.txt"
st2 = "merger2.txt"
st3 = "rank_nodes_pagerank_without_weight.txt"
st4 = "inverse_rankings.txt"
st5 = "time_diff.txt"
st6 = "ans_count.txt"
st7 = "nlp_score.txt"

nooffeatures = 12
directed_graph = nx.DiGraph()
pagerank_dict = {}
leader_fol_dict = {}
bw_centrality = {}
accepted_answer_id = {}
time_diff_of_accepted = {}
nlp_dict = {}
degree = {}
degsu = 1

graph_file = open(st1)
for line in graph_file:
  try: 
	    v1 = int(line.split(" ")[0])
	    v2 = int(line.split(" ")[1])
	    directed_graph.add_edge(v1, v2)
	    
	    if( v1 in degree ):
	        degree[v1] += 1
	    else:
	        degree[v1] = 1
	    if( v2 in degree ):
	        degree[v2] += 1
	        degsu = max(degsu, degree[v2])
	    else:
	        degree[v2] = 1
  except Exception:
	  	pass

for key, value in degree.items():
   degree[key] = float(value)/degsu

pagerank_file = open(st3)
for line in pagerank_file:
   try: 
	    v1 = int(line.split(" ")[0])
	    pagerankk = float(line.split(" ")[1])
	    #pagerankk = "%.8f" % ( float(line.split(" ")[1]) )
	    pagerank_dict[ v1 ] = pagerankk
   except Exception:
   		pass

max1 = 0
leader_follower_file = open(st4)
for line in leader_follower_file:
   try:
	    v1 = int(line.split(" ")[0])
	    leader_fol_score = float(line.split(" ")[1])
	    max1 = max(max1, leader_fol_score)
   except Exception:
	    pass 

leader_follower_file = open(st4)
for line in leader_follower_file:
   try: 
	    v1 = int(line.split(" ")[0])
	    leader_fol_score = float(line.split(" ")[1])
	    leader_fol_dict[ v1 ] = float(leader_fol_score)/max1
   except Exception:
	   	pass

max1 = 0
time_diff_acc = open(st5)
for line in time_diff_acc:
   try: 
	    v1 = int(line.split(" ")[0])
	    v2 = float(line.split(" ")[1])
	    max1 = max(max1, v2)
   except Exception:
	    pass 
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

max1 = 0
nlpp = open(st7)
for line in nlpp:
    v1 = int(line.split(" ")[0])
    v2 = float(line.split(" ")[1])
    max1 = max(max1, v2)

nlpp = open(st7)
for line in nlpp:
    v1 = int(line.split(" ")[0])
    v2 = float(line.split(" ")[1])
    nlp_dict[ v1 ] = float(v2)/max1

def check2( vert ):
    if( vert in accepted_answer_id ):
        return accepted_answer_id[vert]
    return 0

def check3( vert ):
    if( vert in time_diff_of_accepted ):
        return time_diff_of_accepted[vert]
    return 1

def check4( vert ):
    if( vert in nlp_dict ):
        return nlp_dict[vert]
    return 0
        
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
    
    vect.append( check4(vert1) )
    vect.append( check4(vert2) )
        
    return vect

with open("dictidbody.dump", "rb") as fp:   # Unpickling
    dictt = pickle.load(fp)

# load the model back
model_loaded = Doc2Vec.load('mymodel2')

with open("SVM_Classifierso3.dump", "rb") as fp:    # Unpickling
    clf2 = pickle.load(fp)

print('Checking')
correct = 0
noofval = 0
rejected = 0
tested_graph_file = open(st2)
for line in tested_graph_file:
	v1 = int(line.split(" ")[0])
	v2 = int(line.split(" ")[1])
	v3 = int(line.split(" ")[2])       

	token1 = dictt[v1].split()
	new_vector1 = model.infer_vector(token1)
	token2 = dictt[v2].split()
	new_vector2 = model.infer_vector(token2)
	sims1 = model.docvecs.most_similar([new_vector1]) # gives you top 10 document tags and their cosine similarity
	sims2 = model.docvecs.most_similar([new_vector2]) # gives you top 10 document tags and their cosine similarity
	itoj = 0
	jtoi = 0

	for i in sims1:
		for j in sims2:
			img = getfeatures(i[0], j[0])
 
			try:
				labell = clf2.predict([img])
				if( labell==j[0] ):
					itoj += 1
				else:
					jtoi += 1
			except Exception: 
				rejected += 1
				pass
    
	if( v3==v2 ):
		if( itoj>jtoi ):
			correct += 1
	else:
		if( jtoi>itoj ):
			correct += 1

	noofval += 1

print( correct, noofval, rejected )
print( (float(correct)/noofval) )