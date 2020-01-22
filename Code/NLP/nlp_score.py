<<<<<<< HEAD
import pickle
from Question import Question
from loc_score import *

with open("answer_texts_by_question_id4.dump","rb") as f1:
	answers = pickle.load(f1)

# print len(answers)
# for i in answers.keys():
# 	print len(answers[i])
# print len(answers[0])
nlp_score_list=dict()
with open("questions4.dump","rb") as f2:
	questions = pickle.load(f2)
print "Dump Read ..."
f=open("nlp_score.txt","wb")

for ques_id in questions.keys():
	print ques_id,
	ans_list=answers[ques_id]
	tot_score=0
	for ans in ans_list:
		try:
			score = nlp_score(ans)
			if(score!=-1):
				tot_score = tot_score+score
		except:
			pass
	final_score=tot_score/len(ans_list)
	nlp_score_list[ques_id]=final_score
	print final_score
	with open("nlp_score_list.dump","wb") as f3:
		pickle.dump(nlp_score_list,f3)
	f.write(ques_id+" "+str(final_score)+"\n")


=======
import pickle
from Question import Question
from loc_score import *

with open("answer_texts_by_question_id4.dump","rb") as f1:
	answers = pickle.load(f1)

# print len(answers)
# for i in answers.keys():
# 	print len(answers[i])
# print len(answers[0])
nlp_score_list=dict()
with open("questions4.dump","rb") as f2:
	questions = pickle.load(f2)
print "Dump Read ..."
f=open("nlp_score.txt","wb")

for ques_id in questions.keys():
	print ques_id,
	ans_list=answers[ques_id]
	tot_score=0
	for ans in ans_list:
		try:
			score = nlp_score(ans)
			if(score!=-1):
				tot_score = tot_score+score
		except:
			pass
	final_score=tot_score/len(ans_list)
	nlp_score_list[ques_id]=final_score
	print final_score
	with open("nlp_score_list.dump","wb") as f3:
		pickle.dump(nlp_score_list,f3)
	f.write(ques_id+" "+str(final_score)+"\n")


>>>>>>> 0df05ffd4a6d468fed58c4c8c92d5ae333b0c5e0
# f.close()