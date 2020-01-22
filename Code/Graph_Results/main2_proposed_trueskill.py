from trueskill import *
from random import randint
from Question import Question
from common2 import *

print "Total questions", len(questions)
fin_pairs = open("questions/ques_pairs_with_groundtruth.txt")
data_ids = fin_pairs.readlines()
data_ids = ' '.join(data_ids)
fin_pairs.close()

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

def competeAndUpdate(id1, id2):
	rating1 = None
	rating2 = None
	assert(id1 != "-1" and id2 != "-1")
	try:
		rating1 = ratings[id1]
	except KeyError:
		ratings[id1] = Rating()
	try:
		rating2 = ratings[id2]
	except KeyError:
		ratings[id2] = Rating()
	rating1, rating2 = ratings[id1], ratings[id2]
	ratings[id1], ratings[id2] = rate_1vs1(rating1, rating2)

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

for question_id in questions.keys():
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
	for non_best_user in post.non_best_answer_user_ids:
		try:
			for question in user_questions[non_best_user]:
				competeAndUpdate(getQuestionKey(question), post.asker_id)
				competeAndUpdate(getQuestionKey(question), getQuestionKey(question_id))
		except KeyError:
			pass
	try:
		for question in user_questions[post.best_answer_user_id]:
			competeAndUpdate(getQuestionKey(question), post.asker_id)
			competeAndUpdate(getQuestionKey(question), getQuestionKey(question_id))
	except KeyError:
		pass
	for user_id in post.non_best_answer_user_ids:
		competeAndUpdate(post.best_answer_user_id, user_id)
	competeAndUpdate(post.best_answer_user_id, post.asker_id)
	competeAndUpdate(post.best_answer_user_id, getQuestionKey(question_id))
	competeAndUpdate(getQuestionKey(question_id), post.asker_id)

ratings_new = dict()

for rating in ratings.keys():
	if rating is not None and isQuestionKey(rating):
		ratings_new[int(removeQuestionFlag(rating))] = ratings[rating].mu

computeAccuracy(ratings_new)
