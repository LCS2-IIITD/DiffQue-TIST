from bs4 import BeautifulSoup
import pickle
import sys
sys.path.append('..')
from Question import Question


new_so_questions = dict()

fin = open("new_so_posts.xml")
foutq = open("new_so_posts_questions_cleaned.xml", "w")
fouta = open("new_so_posts_answers_cleaned.xml", "w")

# fin = open("../dump/math_posts.xml")
# foutq = open("java_posts_questions_cleaned.xml", "w")
# fouta = open("java_posts_answers_cleaned.xml", "w")


counter = 0
java_question_counter = 0
non_java_question_counter = 0
relevant_answer_counter = 0
non_relevant_answer_counter = 0
rejected = 0
not_accepted_and_not_positive_answer_counter = 0
accepted_answer_counter = 0
positive_answer_counter = 0

owner_deleted_count = 0
questions = dict()
user_questions = dict()
question_non_best_answer_found_flag = dict()
question_best_answer_found_flag = dict()

user_best_answers_question_id = dict()
user_non_best_answers_question_id = dict()
answer_texts_by_question_id = dict()
answer_questionid = dict()



def addQuestionToUser(user_id, question_id):
	try:
		user_questions[user_id]
	except KeyError:
		user_questions[user_id] = []
	user_questions[user_id].append(question_id)

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


for line in fin:
	counter += 1
	if counter % 1000 == 0:
		print counter, rejected, java_question_counter, non_java_question_counter, relevant_answer_counter,accepted_answer_counter, positive_answer_counter, non_relevant_answer_counter, not_accepted_and_not_positive_answer_counter
	line = line.replace("&lt;p&gt;","")
	line = line.replace("&lt;/p&gt;","")

	line = line.replace("&lt;li&gt;","")
	line = line.replace("&lt;/li&gt;","")

	line = line.replace("&lt;ul&gt;","")
	line = line.replace("&lt;/ul&gt;","")

	line = line.replace("&#xA;","")
	line = line.replace("&#xD;","")

	line = line.replace("&quot;","")
	line = line.replace("&lt;","")
	line = line.replace("&gt;","")
	line = line.replace("&amp;","")
	
	try:
		parsed = BeautifulSoup(line)
		if parsed.row["posttypeid"] == "1":
			tags = parsed.row["tags"]
			if "java" in tags and "javascript" not in tags:
				post_type = parsed.row["posttypeid"]
				post_id = parsed.row["id"]
				post_best_answer_id = None
				post_body = parsed.row["body"]
				try:
					post_owner_id = parsed.row["owneruserid"]
				except KeyError:
					owner_deleted_count += 1
					continue
				addQuestionToUser(post_owner_id, post_id)
				try:
					post_best_answer_id = parsed.row["acceptedanswerid"]
				except KeyError:
					post_best_answer_id = None
				if post_owner_id == "-1":
					continue
				new_question = Question(post_id, post_body, post_owner_id, post_best_answer_id)
				questions[post_id] = new_question
				foutq.write(line)
				java_question_counter += 1
				new_so_questions[parsed.row["id"]] = True
			else:
				non_java_question_counter += 1
		if parsed.row["posttypeid"] == "2":
			if parsed.row["parentid"] in new_so_questions:
				post_type = parsed.row["posttypeid"]
				post_id = parsed.row["id"]
				try:
					post_owner_id = parsed.row["owneruserid"]
				except KeyError:
					#User deleted
					continue
				post_parent_id = parsed.row["parentid"]
				post_score = int(parsed.row["score"])
				if post_score > 0:
					positive_answer_counter += 1
				if questions[post_parent_id].best_answer_id == post_id:
					accepted_answer_counter += 1
				if (questions[post_parent_id].best_answer_id == post_id or post_score > 0) is False :
					not_accepted_and_not_positive_answer_counter += 1
					continue
				try:
					addAnswerByQuestion(post_id, parsed.row["body"], post_parent_id)
					if post_id == questions[post_parent_id].best_answer_id:
						questions[post_parent_id].best_answer_user_id = post_owner_id
						addBestAnswer(post_owner_id, post_parent_id)
					else:
						questions[post_parent_id].non_best_answer_user_ids.append(post_owner_id)
						addNonBestAnswer(post_owner_id, post_parent_id)
				except KeyError:
					#Parent post absent
					continue
				fouta.write(line)
				relevant_answer_counter += 1
			else:
				non_relevant_answer_counter += 1
	except:
		rejected += 1
		print "Rejected",rejected


foutq.close()
fouta.close()
fin.close()

with open("valid_test_set_questions.txt", "w") as fp:
	l = []
	for question_id in questions:
		if question_id in question_best_answer_found_flag and question_id in question_non_best_answer_found_flag:
			l.append((len(questions[question_id].non_best_answer_user_ids), question_id))
	l.sort(reverse = True)
	for priority, question_id in l[:1000]:
		fp.write(question_id + '\n')
	# print l[:100]

with open("new_so_user_best_answers_question_id4.dump", "wb") as fp:   #Pickling
	pickle.dump(user_best_answers_question_id, fp)

with open("new_so_user_non_best_answers_question_id4.dump", "wb") as fp:   #Pickling
	pickle.dump(user_non_best_answers_question_id, fp)

with open("new_so_questions4.dump", "wb") as fp:   #Pickling
	pickle.dump(questions, fp)

with open("new_so_user_questions4.dump", "wb") as fp:   #Pickling
	pickle.dump(user_questions, fp)

with open("new_so_answer_texts_by_question_id4.dump", "wb") as fp:   #Pickling
	pickle.dump(answer_texts_by_question_id, fp)

with open("new_so_answer_questionid4.dump", "wb") as fp:   #Pickling
	pickle.dump(answer_questionid, fp)