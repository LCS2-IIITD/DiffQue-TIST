from bs4 import BeautifulSoup
# from trueskill import *
import pickle
import sys
sys.path.append('..')
from Question import Question

# class Question:
# 	def __init__(self, question_id, question_text, asker_id, best_answer_id):
# 		self.question_id = question_id
# 		self.question_text = question_text
# 		self.asker_id = asker_id
# 		self.best_answer_id = best_answer_id
# 		self.best_answer_user_id = None
# 		self.non_best_answer_user_ids = []
# 	def __eq__(self, other):
# 		return other.question_id == self.question_id
# 	def __hash__(self):
# 		return self.question_id

# fin_questions = open("dump/java_posts_6lac_clean_questions_only.xml")
fin_questions = open("../dump/math_posts_questions_cleaned.xml")
questions = dict()
user_questions = dict()
counter = 0
question_non_best_answer_found_flag = dict()
question_best_answer_found_flag = dict()

def addQuestionToUser(user_id, question_id):
	try:
		user_questions[user_id]
	except KeyError:
		user_questions[user_id] = []
	user_questions[user_id].append(question_id)

owner_deleted_count = 0

for line in fin_questions:
	counter += 1
	parsed = BeautifulSoup(line)
	if counter % 1000 == 0:
		print counter
	post_type = parsed.row["posttypeid"]
	post_id = parsed.row["id"]
	post_best_answer_id = None
	post_body = parsed.row["body"]
	try:
		post_owner_id = parsed.row["owneruserid"]
	except KeyError:
		# print "user deleted",post_id
		owner_deleted_count += 1
		continue
		# print "User deleted"
	addQuestionToUser(post_owner_id, post_id)
	try:
		post_best_answer_id = parsed.row["acceptedanswerid"]
	except KeyError:
		pass
	if post_owner_id == "-1":
		continue
	new_question = Question(post_id, post_body, post_owner_id, post_best_answer_id)
	questions[post_id] = new_question


print "Total",owner_deleted_count," have no owneruserid"
fin_questions.close()



def addAnswerByQuestion(answer_id, answer_text, question_id):
	try:
		answer_texts_by_question_id[question_id]
	except KeyError:
		answer_texts_by_question_id[question_id] = []
	answer_texts_by_question_id[question_id].append(answer_text)
	answer_questionid[answer_id] = question_id

def addBestAnswer(user_id, question_id):
	try:
		user_best_answers_question_id[user_id]
	except KeyError:
		user_best_answers_question_id[user_id] = []
	user_best_answers_question_id[user_id].append(question_id)
	question_best_answer_found_flag[question_id] = True

def addNonBestAnswer(user_id, question_id):
	try:
		user_non_best_answers_question_id[user_id]
	except KeyError:
		user_non_best_answers_question_id[user_id] = []
	user_non_best_answers_question_id[user_id].append(question_id)
	question_non_best_answer_found_flag[question_id] = True

user_best_answers_question_id = dict()
user_non_best_answers_question_id = dict()
answer_texts_by_question_id = dict()
answer_questionid = dict()

fin_answers = open("../dump/math_posts_answers_cleaned.xml")
counter = 0
answers_added = 0
for line in fin_answers:
	counter += 1
	parsed = BeautifulSoup(line)
	if counter % 1000 == 0:
		print counter, "Answers added:", answers_added
	post_type = parsed.row["posttypeid"]
	post_id = parsed.row["id"]
	try:
		post_owner_id = parsed.row["owneruserid"]
	except KeyError:
		#User deleted
		continue
	post_parent_id = parsed.row["parentid"]
	try:
		addAnswerByQuestion(post_id, parsed.row["body"], post_parent_id)
		answers_added += 1
		if post_id == questions[post_parent_id].best_answer_id:
			questions[post_parent_id].best_answer_user_id = post_owner_id
			addBestAnswer(post_owner_id, post_parent_id)
		else:
			# if post_parent_id == '1986902':
			# print "Adding", post_parent_id, post_owner_id
			questions[post_parent_id].non_best_answer_user_ids.append(post_owner_id)
			addNonBestAnswer(post_owner_id, post_parent_id)
	except KeyError:
		#Parent post absent
		continue

fin_answers.close()

with open("valid_test_set_questions.txt", "w") as fp:
	l = []
	for question_id in questions:
		if question_id in question_best_answer_found_flag and question_id in question_non_best_answer_found_flag:
			l.append((len(questions[question_id].non_best_answer_user_ids), question_id))
	l.sort(reverse = True)
	for priority, question_id in l[:1000]:
		fp.write(question_id + '\n')
	# print l[:100]

with open("math_user_best_answers_question_id4.dump", "wb") as fp:   #Pickling
	pickle.dump(user_best_answers_question_id, fp)

with open("math_user_non_best_answers_question_id4.dump", "wb") as fp:   #Pickling
	pickle.dump(user_non_best_answers_question_id, fp)

with open("math_questions4.dump", "wb") as fp:   #Pickling
	pickle.dump(questions, fp)

with open("math_user_questions4.dump", "wb") as fp:   #Pickling
	pickle.dump(user_questions, fp)

with open("math_answer_texts_by_question_id4.dump", "wb") as fp:   #Pickling
	pickle.dump(answer_texts_by_question_id, fp)

with open("math_answer_questionid4.dump", "wb") as fp:   #Pickling
	pickle.dump(answer_questionid, fp)