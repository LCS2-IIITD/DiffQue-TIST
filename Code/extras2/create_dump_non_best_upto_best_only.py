from bs4 import BeautifulSoup
# from trueskill import *
import pickle
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
fin_questions = open("dump/java_posts_1lac_clean_questions_only.xml")
questions = dict()
counter = 0
for line in fin_questions:
	counter += 1
	parsed = BeautifulSoup(line,  "lxml")
	if counter % 1000 == 0:
		print counter
	post_type = parsed.row["posttypeid"]
	post_id = parsed.row["id"]
	post_best_answer_id = None
	try:
		post_body = parsed.row["body"]
		post_owner_id = parsed.row["owneruserid"]
		try:
			post_best_answer_id = parsed.row["acceptedanswerid"]
		except:
			pass
		if post_owner_id == "-1":
			raise IOError
	except:
		continue
		# print "User deleted or no accepted answer"
	new_question = Question(post_id, post_body, post_owner_id, post_best_answer_id)
	questions[post_id] = new_question

fin_questions.close()



user_best_answers_question_id = dict()
user_non_best_answers_question_id = dict()

def addBestAnswer(user_id, question_id):
	try:
		user_best_answers_question_id[user_id]
	except:
		user_best_answers_question_id[user_id] = []
	user_best_answers_question_id[user_id].append(question_id)

def addNonBestAnswer(user_id, question_id):
	try:
		user_non_best_answers_question_id[user_id]
	except:
		user_non_best_answers_question_id[user_id] = []
	user_non_best_answers_question_id[user_id].append(question_id)


fin_answers = open("dump/java_posts_1lac_clean_answers_only.xml")
counter = 0
non_best_removed = 0
for line in fin_answers:
	counter += 1
	parsed = BeautifulSoup(line,  "lxml")
	if counter % 1000 == 0:
		print counter
	try:
		post_type = parsed.row["posttypeid"]
	except:
		#some formatting error, example at line 55076, Id: 1963924
		print "formatting error"
		continue
	post_id = parsed.row["id"]
	try:
		post_owner_id = parsed.row["owneruserid"]
	except:
		#User deleted
		continue
	post_parent_id = parsed.row["parentid"]
	post_score = int(parsed.row["score"])
	try:
		if post_id == questions[post_parent_id].best_answer_id:
			questions[post_parent_id].best_answer_user_id = post_owner_id
			addBestAnswer(post_owner_id, post_parent_id)
		elif questions[post_parent_id].best_answer_user_id is None and post_score >= 0:
			# if post_parent_id == '1986902':
			# print "Adding", post_parent_id, post_owner_id
			questions[post_parent_id].non_best_answer_user_ids.append(post_owner_id)
			addNonBestAnswer(post_owner_id, post_parent_id)
		else:
			non_best_removed += 1
	except:
		#Parent post absent
		continue

print "Non best removed", non_best_removed

with open("user_best_answers_question_id3.dump", "wb") as fp:   #Pickling
	pickle.dump(user_best_answers_question_id, fp)

with open("user_non_best_answers_question_id3.dump", "wb") as fp:   #Pickling
	pickle.dump(user_non_best_answers_question_id, fp)

with open("questions3.dump", "wb") as fp:   #Pickling
	pickle.dump(questions, fp)
