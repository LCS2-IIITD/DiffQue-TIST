# import numpy
# from numpy import *
from Question import Question
import common2
from common2 import *
import pickle
import networkx as nx
from networkx.exception import NetworkXError	
from hits_nx import hits_nx

graph = []

fin_pairs = open("questions/ques_pairs_with_groundtruth.txt")
lines = fin_pairs.readlines()
lines = ' '.join(lines)
fin_pairs.close()

asker_to_asker_question=[]
asker_question_to_best_answer_user=[]
asker_question_to_all_non_best_answers_user=[]
asker_to_best_answer_user=[]
asker_to_all_non_best_answer_user=[]
asker_question_to_best_answerer_user_questions =[]

with open("dump2/questions4.dump", "rb") as fp:   # Unpickling
	questions = pickle.load(fp)

with open("edges_dump/asker_to_asker_question.dump", "rb") as fp:   #Pickling
	asker_to_asker_question = pickle.load(fp)

with open("edges_dump/asker_question_to_best_answer_user.dump", "rb") as fp:   #Pickling
	asker_question_to_best_answer_user = pickle.load(fp)

with open("edges_dump/asker_question_to_all_non_best_answers_user.dump", "rb") as fp:   #Pickling
	asker_question_to_all_non_best_answers_user = pickle.load(fp)

# with open("edges_dump/asker_to_best_answer_user.dump", "rb") as fp:   #Pickling
# 	asker_to_best_answer_user = pickle.load(fp)

# with open("edges_dump/asker_to_all_non_best_answer_user.dump", "rb") as fp:   #Pickling
# 	asker_to_all_non_best_answer_user = pickle.load(fp)

with open("edges_dump/asker_question_to_best_answerer_user_questions.dump", "rb") as fp:   #Pickling
	asker_question_to_best_answerer_user_questions = pickle.load(fp)

edges=asker_to_asker_question+asker_question_to_best_answer_user+asker_question_to_best_answer_user+asker_question_to_best_answer_user+asker_question_to_best_answer_user+asker_question_to_best_answer_user



G=nx.Graph()

for edge in edges:
	G.add_edge(*edge)

h,a=hits_nx(G)
# print h,a

difficulty = dict()
for i in questions.keys():
	if(h.has_key(int(i))):
		difficulty[int(i)] = h[int(i)]
	else:
		difficulty[int(i)]=0
computeAccuracy(difficulty)
