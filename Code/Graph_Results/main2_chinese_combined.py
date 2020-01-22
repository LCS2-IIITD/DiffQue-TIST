import pagerank
from Question import Question
from common2 import *
from trueskill import *
from compute_accuracy_from_js_output import computeAccuracyFromJSOutput
from os.path import isfile
from sys import argv
from random import sample
percentage_edges_to_sample = 0.30

def getEdgesFileLocation():
	if len(argv) >= 3:
		network = argv[2]
	filename = "edges_chinese_"+dataset+".txt"
	if isfile(filename) == False:
		print "Edges file doesn't exist!"
		assert(False)
	return filename

graph = []
edges_dict = {}

def addEdge(e):
	if e not in edges_dict:
		edges_dict[e] = True
		graph.append(e)

def getEdgesFileLocation():
    filename = "edges_chinese_"+dataset+".txt"
    if isfile(filename) == False:
        print "Edges file doesn't exist!"
        assert(False)
    return filename


filename = 'edges_chinese_' + dataset + '.txt'
if isfile(filename) == False:
    counter = 0
    for user in user_questions.keys(): #iterate over the users
    	counter += 1
    	if counter % 100 == 0:
    		print counter, len(graph)
    	try:
    		non_best_answers = user_non_best_answers_question_id[user]
    		best_answers = user_best_answers_question_id[user]
    	except:
    		continue
    	for best_answer_question_id in best_answers:
    		for non_best_answer_question_id in non_best_answers:
    			addEdge((int(non_best_answer_question_id), int(best_answer_question_id)))
else:
    with open(getEdgesFileLocation(), "r") as fp:
        for line in fp:
            line = line.rstrip()
            v1 = int(line.split(" ")[0])
            v2 = int(line.split(" ")[1])
            addEdge((v1, v2))
    graph = sample(graph, int(percentage_edges_to_sample * len(graph)))




#TRUESKILL
print "Processing for trueskill"
ratings = dict()
for e in graph:
    v1 = e[0]
    v2 = e[1]
    ratings[v1] = Rating()
    ratings[v2] = Rating()

edges_dict2 = {}
counter = 0
for (v1, v2) in graph:
    counter += 1
    if counter % 1000 == 0:
        print counter
    if (v1, v2) not in edges_dict2:
        ratings[v2], ratings[v1] = rate_1vs1(ratings[v2], ratings[v1])
        edges_dict2[(v1, v2)] = True

for rating in ratings:
    ratings[rating] = ratings[rating].mu

print "Computing accuracy for trueskill"
computeAccuracy(ratings)


print "Processing for HITS"
G=nx.Graph()

for edge in graph:
    G.add_edge(*edge)

h,a=hits_nx(G)

difficulty = dict()
for i in questions.keys():
    if(h.has_key(int(i))):
        difficulty[int(i)] = h[int(i)]
    else:
        difficulty[int(i)]=0

print "Computing accuracy for HITS"
computeAccuracy(difficulty)

print "Processing for PageRank"

filename = 'edges_chinese_' + dataset + '.txt'
rank_file = 'chinese_'+dataset+'_ranks.txt'

print "Writing edges for PageRank as",filename
f = open(filename,'w')
for edge in graph:
  f.write(str(edge[0]) + " " + str(edge[1]) + "\n")

f.close()

RemoveNewLine(filename, filename)

print "Processing npm"

system('rm '+rank_file)
system("cp " + filename + ' Temporal/page_rank/')
system('cd Temporal/page_rank && npm start ' + filename + ' '+ rank_file + '&& cp ' + rank_file +' ../../')

print "Computing final rank for PageRank"

computeAccuracyFromJSOutput(rank_file)
