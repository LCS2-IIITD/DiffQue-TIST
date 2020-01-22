from trueskill import *
import pagerank
from Question import Question
from common2 import *

graph = []
edges_dict = {}

def addEdge(e):
	if e not in edges_dict:
		edges_dict[e] = True
		graph.append(e)


counter = 0
for user in user_questions.keys(): #iterate over the users
	counter += 1
	if counter % 100 == 0:
		print counter, "# edges:", len(graph)
	try:
		non_best_answers = user_non_best_answers_question_id[user]
		best_answers = user_best_answers_question_id[user]
	except:
		continue
	for best_answer_question_id in best_answers:
		for non_best_answer_question_id in non_best_answers:
			addEdge((int(non_best_answer_question_id), int(best_answer_question_id)))

# from hits_nx import hits_nx
# import networkx as nx

# G=nx.Graph()

# for edge in graph:
#     G.add_edge(*edge)

# h,a=hits_nx(G)

# difficulty = dict()
# for i in questions.keys():
#     if(h.has_key(int(i))):
#         difficulty[int(i)] = h[int(i)]
#     else:
#         difficulty[int(i)]=0

# computeAccuracy(difficulty)

ratings = {}

counter = 0
for (v1, v2) in graph:
	counter += 1
	if counter % 1000 == 0:
		print counter
	if v1 not in ratings:
		ratings[v1] = Rating()
	if v2 not in ratings:
		ratings[v2] = Rating()
	ratings[v2], ratings[v1] = rate_1vs1(ratings[v2], ratings[v1])




f = open('edges_chinese.txt','w')
for edge in graph:
  f.write(str(edge[0]) + " " + str(edge[1]) + "\n")

f.close()


# ratings = pagerank.pagerank(graph)[0]

computeAccuracy(ratings)

