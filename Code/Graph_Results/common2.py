import pickle
from Question import Question
from random import randint
from sklearn.metrics import f1_score
from sklearn import metrics
from hits_nx import hits_nx
import networkx as nx
from removenewline import RemoveNewLine
from os import system
from sys import argv
import sys

questions = dict()

user_best_answers_question_id = dict()
user_non_best_answers_question_id = dict()

computeF1 = True


#Global setting for dataset. Note that changing the dataset here is enough AFAIK
dataset = "old" #choose "math", "old" or "new"
if len(argv) >= 2:
	dataset = argv[1]


print "Dataset in use is",dataset

sys.stdout.flush()

if dataset == "old":
	with open("dump2/old_so/old_so_questions4.dump", "rb") as fp:   # Unpickling
		questions = pickle.load(fp)
	with open("dump2/old_so/old_so_user_best_answers_question_id4.dump", "rb") as fp:   # Unpickling
		user_best_answers_question_id = pickle.load(fp)
	with open("dump2/old_so/old_so_user_non_best_answers_question_id4.dump", "rb") as fp:   # Unpickling
		user_non_best_answers_question_id = pickle.load(fp)
	with open("dump2/old_so/old_so_user_questions4.dump", "rb") as fp:   # Unpickling
		user_questions = pickle.load(fp)
elif dataset == "new":
	with open("dump2/new_so/new_so_questions4.dump", "rb") as fp:   # Unpickling
		questions = pickle.load(fp)
	with open("dump2/new_so/new_so_user_best_answers_question_id4.dump", "rb") as fp:   # Unpickling
		user_best_answers_question_id = pickle.load(fp)
	with open("dump2/new_so/new_so_user_non_best_answers_question_id4.dump", "rb") as fp:   # Unpickling
		user_non_best_answers_question_id = pickle.load(fp)
	with open("dump2/new_so/new_so_user_questions4.dump", "rb") as fp:   # Unpickling
		user_questions = pickle.load(fp)
elif dataset == "math":
	with open("dump2/math/math_questions4.dump", "rb") as fp:   # Unpickling
		questions = pickle.load(fp)
	with open("dump2/math/math_user_best_answers_question_id4.dump", "rb") as fp:   # Unpickling
		user_best_answers_question_id = pickle.load(fp)
	with open("dump2/math/math_user_non_best_answers_question_id4.dump", "rb") as fp:   # Unpickling
		user_non_best_answers_question_id = pickle.load(fp)
	with open("dump2/math/math_user_questions4.dump", "rb") as fp:   # Unpickling
		user_questions = pickle.load(fp)
elif dataset == "mid":
	with open("dump2/mid_so/mid_so_questions4.dump", "rb") as fp:   # Unpickling
		questions = pickle.load(fp)
	with open("dump2/mid_so/mid_so_user_best_answers_question_id4.dump", "rb") as fp:   # Unpickling
		user_best_answers_question_id = pickle.load(fp)
	with open("dump2/mid_so/mid_so_user_non_best_answers_question_id4.dump", "rb") as fp:   # Unpickling
		user_non_best_answers_question_id = pickle.load(fp)
	with open("dump2/mid_so/mid_so_user_questions4.dump", "rb") as fp:   # Unpickling
		user_questions = pickle.load(fp)
else:
	print "Dataset invalid"
	assert(False)


# with open("dump2/answer_texts_by_question_id4.dump", "rb") as fp:   # Unpickling
# 	answer_texts_by_question_id4 = pickle.load(fp)


def computeAccuracyAndF1AndAUC(ratings):
	global dataset
	fin_pairs = open("questions/ground_truth/" + dataset+ ".txt") #Kindly put all the three files in this directory, named as per the possible values of dataset writen at its declaration
	print "Same rating pairs(if any) :"
	correct = 0.0
	incorrect = 0.0
	rejected1 = 0
	rejected2 = 0
	y_true = []
	y_pred = []
	for line in fin_pairs:
		if len(line.split(" ")) <= 2:
			continue
		line = line.rstrip()
		id1 = line.split(" ")[0]
		id2 = line.split(" ")[1]
		better_id = line.split(" ")[2]
		rating1 = None
		rating2 = None
		try:
			rating1 = ratings[int(id1)]
		except:
			rejected1 += 1
			continue
		try:
			rating2 = ratings[int(id2)]
		except:
			rejected1 += 1
			continue
		if better_id == id1:
			y_true.append(0)
		elif better_id == id2:
			y_true.append(1)
		else:
			assert(False)
		if rating1 > rating2:
			y_pred.append(0)
		elif rating2 > rating1:
			y_pred.append(1)
		else:
			r = randint(0, 1) #Randomly predict more difficult question
			y_pred.append(r)
		if rating1 > rating2 and better_id == id1:
			correct += 1
		elif rating2 > rating1 and better_id == id2:
			correct += 1
		else:
			# temp_file.write(id1+" "+id2+"\n")
			# print id1,id2
			if rating1 == rating2:
				print id1, id2
				rejected2 += 1
				r = randint(1, 2) #Randomly predict more difficult question
				if r == 1 and better_id == id1:
					correct += 1
				elif r == 2 and better_id == id2:
					correct += 1
				else:
					incorrect += 1
			else:
				# print id1, id2, better_id
				incorrect += 1
			# if rating1 == rating2:
			# 	rejected2 += 1
			# 	print "Rating same for",id1,id2
			
	print "Rejected(absentees)", rejected1, "PseudoRejected(same rating)", rejected2
	print "Accuracy", correct/(correct + incorrect), "Analyzed",correct + incorrect
	print "Note that same ratings are randomly assigned a different difficulty!"
	print "F1 Score:", f1_score(y_true, y_pred, average='macro')
	fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred)
	print "AUC:", metrics.auc(fpr, tpr)
	print "Dataset is",dataset
	fin_pairs.close()

def computeAccuracy(ratings):
	global dataset
	print "Dataset in use is",dataset
	if computeF1:
		print "Redirecting to compute both F1 and accuracy"
		computeAccuracyAndF1AndAUC(ratings)
		return
	fin_pairs = open("questions/ques_pairs_with_groundtruth.txt")
	print "Same rating pairs(if any) :"
	correct = 0.0
	incorrect = 0.0
	rejected1 = 0
	rejected2 = 0
	for line in fin_pairs:
		if len(line.split(" ")) <= 2:
			continue
		line = line.rstrip()
		id1 = line.split(" ")[0]
		id2 = line.split(" ")[1]
		better_id = line.split(" ")[2]
		rating1 = None
		rating2 = None
		try:
			rating1 = ratings[int(id1)]
		except:
			rejected1 += 1
			continue
		try:
			rating2 = ratings[int(id2)]
		except:
			rejected1 += 1
			continue
		if rating1 > rating2 and better_id == id1:
			correct += 1
		elif rating2 > rating1 and better_id == id2:
			correct += 1
		else:
			# temp_file.write(id1+" "+id2+"\n")
			# print id1,id2
			if rating1 == rating2:
				print id1, id2
				rejected2 += 1
				r = randint(1, 2) #Randomly predict more difficult question
				if r == 1 and better_id == id1:
					correct += 1
				elif r == 2 and better_id == id2:
					correct += 1
				else:
					incorrect += 1
			else:
				# print id1, id2, better_id
				incorrect += 1
			# if rating1 == rating2:
			# 	rejected2 += 1
			# 	print "Rating same for",id1,id2
			
	print "Accuracy", correct/(correct + incorrect), "Analyzed",correct + incorrect, "Rejected(absentees)", rejected1, "PseudoRejected(same rating)", rejected2
	print "Note that same ratings are randomly assigned a different difficulty!"
	fin_pairs.close()
