from Question import Question
import pagerank
from common2 import *



graph = []

fin_pairs = open("questions/ques_pairs_with_groundtruth.txt")
lines = fin_pairs.readlines()
lines = ' '.join(lines)
fin_pairs.close()


edges_dict = {}
def addEdge(e):
	if e not in edges_dict:
		edges_dict[e] = True
		graph.append(e)


counter = 0
for question_id in questions.keys():
	counter += 1
	if counter % 1000 == 0:
		print counter
	post = questions[question_id]
	for non_best_user in post.non_best_answer_user_ids:
		try:
			for question in user_questions[non_best_user]:
				addEdge((int(question_id), int(question)))
		except KeyError:
			pass
	try:
		for question in user_questions[post.best_answer_user_id]:
			addEdge((int(question_id), int(question)))
	except KeyError:
		pass

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

# ratings = pagerank.pagerank(graph, verbose = True)[0]

# computeAccuracy(ratings)

f = open('edges_basic.txt','w')
for edge in graph:
  f.write(str(edge[0]) + " " + str(edge[1]) + "\n")

f.close()
