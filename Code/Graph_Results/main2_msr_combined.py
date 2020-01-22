from trueskill import *
from random import randint
from Question import Question
from common2 import *
from compute_accuracy_from_js_output import computeAccuracyFromJSOutput



print "Total questions", len(questions)

for question_id in questions.keys():
	if questions[question_id].best_answer_user_id is not None or len(questions[question_id].non_best_answer_user_ids) != 0:
		continue
	else:
		del questions[question_id]
	# if question_id not in data_ids:
	# 	del questions[question_id]
	# 	continue
	# if questions[question_id].best_answer_user_id is None and len(questions[question_id].non_best_answer_user_ids) == 0:
	# 	del questions[question_id]

print "Useful questions", len(questions)

ratings = dict()
graph = []
error_counter = 0

edges_dict = {}

def competeAndUpdate(id1, id2):
	if (id2, id1) in edges_dict:
		return
	edges_dict[(id2, id1)] = True
	global error_counter
	rating1 = None
	rating2 = None
	assert(id1 != "-1" and id2 != "-1")
	try:
		rating1 = ratings[id1]
		rating2 = ratings[id2]
	except:
		print "ids not present in ratings dictionary"
		print id1, id2
		return
	ratings[id1], ratings[id2] = rate_1vs1(rating1, rating2)
	if id1 is not None and id2 is not None:
		graph.append((id2, id1))
	else:
		error_counter += 1

question_flag = "q"

def getQuestionKey(qid):
	return question_flag + qid

def isQuestionKey(qid):
	return qid.startswith(question_flag)

def removeQuestionFlag(qid):
	if isQuestionKey(qid):
		ending_index = qid.find(question_flag) + len(question_flag)
		return qid[ending_index:]
	else:
		assert(False)

counter = 0
for question_id in questions.keys():
	counter += 1
	if counter % 1000 == 0:
		print counter
	post = questions[question_id]
	for user_id in post.non_best_answer_user_ids:
		ratings[user_id] = Rating()
	ratings[getQuestionKey(question_id)] = Rating()
	ratings[post.best_answer_user_id] = Rating()
	ratings[post.asker_id] = Rating()

counter = 0
for question_id in questions.keys():
	counter += 1
	if counter % 1000 == 0:
		print counter
	post = questions[question_id]
	for user_id in post.non_best_answer_user_ids:
		competeAndUpdate(post.best_answer_user_id, user_id)
	competeAndUpdate(post.best_answer_user_id, post.asker_id)
	competeAndUpdate(post.best_answer_user_id, getQuestionKey(question_id))
	competeAndUpdate(getQuestionKey(question_id), post.asker_id)


print "Adding edges for HITS"
G=nx.Graph()

for edge in graph:
    G.add_edge(*edge)

h,a=hits_nx(G)

difficulty = dict()
for i in questions.keys():
    if(h.has_key(getQuestionKey(i))):
        difficulty[int(i)] = h[getQuestionKey(i)]
    else:
        difficulty[int(i)]=0

print "Computing difficulty for HITS"
computeAccuracy(difficulty)

print "Processing for trueskill"
ratings_new = dict()

for rating in ratings.keys():
	if rating is not None and isQuestionKey(rating):
		ratings_new[int(removeQuestionFlag(rating))] = ratings[rating].mu

print "Computing difficulty for trueskill"
computeAccuracy(ratings_new)


print "Processing for PageRank"

filename = 'edges_msr_' + dataset + '.txt'
correct_filename = 'edges_msr_' + dataset + '_correct.txt'
rank_file = 'msr_'+dataset+'_ranks.txt'
correct_rank_file = 'msr_'+dataset+'_correct_ranks.txt'

print "Writing edges for PageRank as",filename
f = open(filename,'w')
for edge in graph:
  f.write(str(edge[0]) + " " + str(edge[1]) + "\n")

f.close()



fin = open(filename)
fout = open(correct_filename, 'w')
old_name_to_new_name = dict()
new_name_to_old_name = dict()
next_free_id = 1
for line in fin:
	v1 = line.strip().rstrip().split(" ")[0]
	v2 = line.strip().rstrip().split(" ")[1]
	if v1 not in old_name_to_new_name:
		old_name_to_new_name[v1] = str(next_free_id)
		new_name_to_old_name[str(next_free_id)] = v1
		next_free_id += 1
	if v2 not in old_name_to_new_name:
		old_name_to_new_name[v2] = str(next_free_id)
		new_name_to_old_name[str(next_free_id)] = v2
		next_free_id += 1
	fout.write(str(old_name_to_new_name[v1]) + ' ' + str(old_name_to_new_name[v2]) + '\n')

fout.close()
fin.close()

RemoveNewLine(correct_filename, correct_filename)


# inp = 'T'
# while inp != 'done':
# 	inp = raw_input("File written as ", correct_filename, "Kindly run the node counterpart using this file and place final file here as rank_nodes_pagerank_without_weight.txt, then type 'done'")

print "Processing npm"

system('rm '+correct_rank_file)
system("cp " + correct_filename + ' Temporal/page_rank/')
system('cd Temporal/page_rank && npm start ' + correct_filename + ' '+ rank_file + '&& cp ' + rank_file +' ../../')

print "npm done, processing results"

fin = open(rank_file)
fout = open(correct_rank_file, 'w')
for line in fin:
	v = line.strip().rstrip().split(" ")[0]
	value = line.strip().rstrip().split(" ")[1]
	if new_name_to_old_name[v].startswith("q"):
		fout.write(new_name_to_old_name[v][1:] + " " + value + '\n')

fout.close()
fin.close()

print "Computing final rank for PageRank"

computeAccuracyFromJSOutput(correct_rank_file)