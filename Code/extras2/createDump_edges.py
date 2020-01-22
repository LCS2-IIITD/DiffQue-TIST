# import numpy
# from numpy import *
from Question import Question
import common2
from common2 import *


graph1=[]
graph2=[]
graph3=[]
graph4=[]
graph5=[]
graph6=[]

counter = 0
for question_id in questions.keys():
	counter += 1
	if counter % 1000 == 0:
		print counter

	post = questions[question_id]

	non_best_answer_user_ids=[]
	best_answer_user_id=None
	question_list_of_best_answerer=[]
	ques_asker=post.asker_id
	if post.best_answer_user_id is not None:
		best_answer_user_id = post.best_answer_user_id
	non_best_answer_user_ids=post.non_best_answer_user_ids
	if(best_answer_user_id is not None):
		for j in user_best_answers_question_id.keys():
			if(j==best_answer_user_id):
				question_list_of_best_answerer = user_best_answers_question_id[best_answer_user_id]	
				break


	# asker to asker-question
	graph1.append((int(ques_asker),int(question_id)))
	
	
	# asker question to best-answer user
	if post.best_answer_user_id is not None:
		graph2.append((int(question_id),int(best_answer_user_id)))
	

	# asker question to all non-best-answers users
	if(len(non_best_answer_user_ids)!=0):
		for q in non_best_answer_user_ids:
			graph3.append((int(question_id),int(q)))
	

	# asker to best-answer user
	if best_answer_user_id is not None:
		graph4.append((int(ques_asker),int(best_answer_user_id)))
	

	# asker to all non-best-answer users
	for k in non_best_answer_user_ids:
		graph5.append((int(ques_asker),int(k)))
	

	# asker-question to non-best-answerer-user-question(s) 
	for z in question_list_of_best_answerer:
		graph6.append((int(question_id),int(z)))


with open("edges_dump/asker_to_asker_question.dump", "wb") as fp:   #Pickling
	pickle.dump(graph1, fp)
with open("edges_dump/asker_question_to_best_answer_user.dump", "wb") as fp:   #Pickling
	pickle.dump(graph2, fp)
with open("edges_dump/asker_question_to_all_non_best_answers_user.dump", "wb") as fp:   #Pickling
	pickle.dump(graph3, fp)
with open("edges_dump/asker_to_best_answer_user.dump", "wb") as fp:   #Pickling
	pickle.dump(graph4, fp)
with open("edges_dump/asker_to_all_non_best_answer_user.dump", "wb") as fp:   #Pickling
	pickle.dump(graph5, fp)
with open("edges_dump/asker_question_to_best_answerer_user_questions.dump", "wb") as fp:   #Pickling
	pickle.dump(graph6, fp)


