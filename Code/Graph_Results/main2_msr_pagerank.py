from trueskill import *
from random import randint
from Question import Question
from common2 import *
from pagerank import pagerank

# print "Total questions", len(questions)
# fin_pairs = open("questions/ques_pairs_with_groundtruth.txt")
# data_ids = fin_pairs.readlines()
# data_ids = ' '.join(data_ids)
# fin_pairs.close()

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

graph = []
error_counter = 0

def competeAndUpdate(id1, id2):
	global error_counter
	# rating1 = None
	# rating2 = None
	# assert(id1 != "-1" and id2 != "-1")
	# try:
	# 	rating1 = ratings[id1]
	# 	rating2 = ratings[id2]
	# except:
	# 	print "ids not present in ratings dictionary"
	# 	print id1, id2
	# 	return
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
		print counter, "One node undefined for # nodes:", error_counter
	post = questions[question_id]
	for user_id in post.non_best_answer_user_ids:
		competeAndUpdate(post.best_answer_user_id, user_id)
	competeAndUpdate(post.best_answer_user_id, post.asker_id)
	competeAndUpdate(post.best_answer_user_id, getQuestionKey(question_id))
	competeAndUpdate(getQuestionKey(question_id), post.asker_id)

# ratings = pagerank(graph)[0]

# ratings_new = dict()

# for rating in ratings.keys():
# 	if rating is not None and isQuestionKey(rating):
# 		ratings_new[int(removeQuestionFlag(rating))] = ratings[rating]

# computeAccuracy(ratings_new)

f = open('edges_msr.txt','w')
for edge in graph:
  f.write(str(edge[0]) + " " + str(edge[1]) + "\n")

f.close()