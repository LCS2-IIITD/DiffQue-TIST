from Question import Question
from common2 import *
import numpy as np
from bs4 import BeautifulSoup
import pickle
from os.path import isfile
from random import sample
from nltk.corpus import stopwords
import math
from sys import argv

n_questions_to_sample = 10000
stops = set(stopwords.words("english"))
lambda1 = 0.1
lambda2 = 0.1
m_users = None
n_questions = None

def getQuestionsFile():
	if dataset == "new":
		return "dump2/new_so/new_so_posts_questions_cleaned.xml"
	elif dataset == "old":
		return "dump2/old_so/old_so_posts_questions_cleaned.xml"
	elif dataset == "mid":
		return "dump2/mid_so/mid_so_posts_questions_cleaned.xml"
	elif dataset == "math":
		return "dump2/math/math_posts_questions_cleaned.xml"
	else:
		assert(False)



def getQuestionTextDumpLocation():
	if dataset == "new":
		return "dump2/new_so/new_so_question_title_body.dump"
	elif dataset == "old":
		return "dump2/old_so/old_so_question_title_body.dump"
	elif dataset == "mid":
		return "dump2/mid_so/mid_so_question_title_body.dump"
	elif dataset == "math":
		return "dump2/math/math_question_title_body.dump"
	else:
		assert(False)



def getEdgesFileLocation():
	network = "msr"
	if len(argv) >= 3:
		network = argv[2]
	filename = "edges_" + network +"_"+dataset+".txt"
	if isfile(filename) == False:
		print "Edges file doesn't exist!"
		assert(False)
	return filename


def getGroundTruthFile():
	return "questions/ground_truth/" + dataset+ ".txt"

def createDump():
	fin = open(getQuestionsFile())
	question_title_body_by_id = {}
	counter = 0
	rejected = 0
	for line in fin:
		counter += 1
		if counter % 1000 == 0:
			print counter, rejected
		try:
			line = line.lower()
			parsed = BeautifulSoup(line)
			post_id = parsed.row["id"]
			post_body = parsed.row["body"]
			post_title = parsed.row["title"]
			question_title_body_by_id[post_id] = post_title + " " + post_body
		except TypeError:
			rejected += 1
	with open(getQuestionTextDumpLocation(), "wb") as fp:
		pickle.dump(question_title_body_by_id, fp)

def getQuestionsFromGroundTruth():
	questions = {}
	fin = open(getGroundTruthFile())
	for line in fin:
		line = line.rstrip()
		v1 = line.split(" ")[0]
		v2 = line.split(" ")[1]
		questions[v1] = True
		questions[v2] = True
	return questions.keys()


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


def initializeSimilarity():
	global question_title_body_by_id, question_ids
	word_freq = {}
	for question_id in question_ids:
		text = question_title_body_by_id[question_id]
		words = text.split(" ")
		for word in words:
			if word in word_freq:
				word_freq[word] += 1
			else:
				word_freq[word] = 1
	for word in word_freq:
		if word_freq[word] < 10:
			if word not in stops:
				stops.add(word)


clean_words = {}
similarity_errors = 0

def getSimilarity(question_id1, question_id2):
	global similarity_errors
	clean_words1 = None
	clean_words2 = None
	try:
		if question_id1 in clean_words:
			clean_words1 = clean_words[question_id1]
		else:
			words1 = question_title_body_by_id[question_id1].split(" ")
			clean_words1 = set([w for w in words1 if not w in stops])
			clean_words[question_id1] = clean_words1
		if question_id2 in clean_words:
			clean_words2 = clean_words[question_id2]
		else:	
			words2 = question_title_body_by_id[question_id2].split(" ")
			clean_words2 = set([w for w in words2 if not w in stops])
			clean_words[question_id2] = clean_words2
	except KeyError:
		similarity_errors += 1
		print "KeyError during similarity. Probably question not found in dict. Count", similarity_errors
		print question_id1, question_id2
		return 0
	union_words = clean_words1.union(clean_words2)
	intersection_words = clean_words1.intersection(clean_words2)
	if len(union_words) == 0:
		return 0
	return len(intersection_words)/float(len(union_words))


def calculateL(C,Z,theta,p,m = m_users, n = n_questions):
	sum_term = 0
	for edge in C:
		temp=m+n
		x_k = np.zeros(temp)
		x_k[edge[0]]=1
		x_k[edge[1]]=-1
		y_k = -1
		#print "x_k shape",x_k.shape
		#print "theta shape",theta.shape
		value = 1 - (y_k*(np.dot(theta, x_k)))
		#print "value in calculateL"
		#print value
		sq_term=max(0,value)
		sum_term = sum_term +math.pow(sq_term,p)
	#L=sum_term + (0.5)*np.transpose(theta)*Z*theta
	L=sum_term + 0.5 * np.dot(np.dot(theta,Z),theta)
	return L


def calculateDeltaL(p,Z,K,theta, m = m_users, n = n_questions):
	temp=m+n
	sum_term1=0
	sum_term2=0
	if(p==1):
		for edge in K:
			x_k = np.zeros(temp)
			x_k[edge[0]] = 1
			x_k[edge[1]] = -1
			y_k = -1
			sum_term1 = sum_term1 + (y_k*x_k)
		delta_L = np.dot(Z,theta) - sum_term1
	else:
		for edge in K:
			x_k = np.zeros(temp)
			x_k[edge[0]]=1
			x_k[edge[1]]=-1
			y_k = -1
			sum_term1 = sum_term1 + x_k*np.transpose(x_k)*theta
			sum_term2 = sum_term2 + y_k*x_k
		delta_L = Z*theta + 2*sum_term1 - 2*sum_term2
	return delta_L



def calculateK(C,theta, m = m_users, n = n_questions):
	K=[]
	temp=m+n
	for edge in C:
		x_k = np.zeros(temp)
		x_k[edge[0]] = 1
		x_k[edge[1]] = -1
		y_k = -1
		#tt=np.transpose(theta)
		#print theta.shape
		#print x_k.shape
		value = 1-(y_k*(np.dot(theta,x_k)))
		#print value
		if(value>0):
			K.append(edge)
	return K


def algo(C,Z,m,n):
	lr=0.001
	T=1000
	p=1
	temp=m+n
	theta=np.ones(temp)
	theta_list=[]
	#put theta(0) and L(0) in respective list.
	theta_list.append(theta)
	L = calculateL(C,Z,theta,p,m,n)
	L_list = np.array(L)
	print "Working on core algorithm"
	for t in range(0,T):
		if t%10 == 0:
			print t
		K=calculateK(C,theta_list[t],m,n)
		#print "In Algo----"
		delta_L = calculateDeltaL(p,Z,K,theta_list[t],m,n)
		#print "delta L shape",delta_L.shape
		next_theta=theta_list[t]-(lr*delta_L)
		#print "next theta shape",next_theta.shape
		theta_list.append(next_theta)
		#print "list[t+1] shape", theta_list[t+1].shape
		L = calculateL(C,Z,next_theta,p,m,n)
		L_list = np.append(L_list,L)
		#print "L-List", L_list
		min_index = np.argmin(L_list)
		#print "min_index",min_index
		theta_list[t+1] = theta_list[min_index]
	return theta_list[T]




if isfile(getQuestionTextDumpLocation()):
	pass #Dump already exists
else:
	createDump() 

with open(getQuestionTextDumpLocation(), "rb") as fp:
	question_title_body_by_id = pickle.load(fp)

#question_ids = []
#The following two lines are for actual use. Comment during testing algo().
question_ids = question_title_body_by_id.keys()
question_ids = sample(question_ids, n_questions_to_sample)
question_ids = list(set(question_ids + getQuestionsFromGroundTruth()))

if '1877592' in question_ids: #some problem with this question in math dataset. Hence, removed.
	question_ids.remove('1877592')

alias_to_id = {}
id_to_alias = {}
alias_counter = 0
new_question_ids = []
C = []

def createMappingAndGetAlias(id1):
	global alias_counter
	if id1 in id_to_alias:
		return id_to_alias[id1]
	id_to_alias[id1] = alias_counter
	alias_to_id[alias_counter] = id1
	alias = alias_counter
	alias_counter += 1
	return alias

def getAlias(id1):
	return id_to_alias[id1]

def getId(alias):
	return alias_to_id[alias]

with open(getEdgesFileLocation(), "r") as fp:
	for line in fp:
		line = line.rstrip()
		v1 = line.split(" ")[0]
		v2 = line.split(" ")[1]
		if isQuestionKey(v1) == False and (isQuestionKey(v2) and removeQuestionFlag(v2) in question_ids):
			createMappingAndGetAlias(v1)
		if isQuestionKey(v2) == False and (isQuestionKey(v1) and removeQuestionFlag(v1) in question_ids):
			createMappingAndGetAlias(v2)

m_users = len(id_to_alias)
print "Number of users", m_users

with open(getEdgesFileLocation(), "r") as fp:
	for line in fp:
		line = line.rstrip()
		v1 = line.split(" ")[0]
		v2 = line.split(" ")[1]
		if (isQuestionKey(v1) and removeQuestionFlag(v1) in question_ids) or (isQuestionKey(v2) and removeQuestionFlag(v2) in question_ids):
			C.append((createMappingAndGetAlias(v1), createMappingAndGetAlias(v2)))

for question_id in question_ids:
	createMappingAndGetAlias(getQuestionKey(question_id))

n_questions = len(id_to_alias) - m_users

print "Number of questions", n_questions

def assertionOfUserQuestionOrdering():
	for id1 in id_to_alias:
		try:
			if isQuestionKey(id1) == False:
				assert(getAlias(id1) < m_users)
			else:
				assert(getAlias(id1) >= m_users and getAlias(id1) < len(id_to_alias))
		except AssertionError:
			print "Assertion of IDs failed for ", id1, isQuestionKey(id1)
			assert(False)


assertionOfUserQuestionOrdering()



# initializeSimilarity()

print "Allocating space for Z matrix. It may crash here. All the best!"
Z = np.zeros((m_users + n_questions, m_users + n_questions))


print "Creating similarity matrix W"

W = np.zeros((n_questions,n_questions))

counter = 0
for iter1 in range(len(question_ids)):
	counter += 1
	if counter % 100 == 0:
		print counter
	question_id1 = question_ids[iter1]
	for iter2 in range(iter1, len(question_ids)):
		question_id2 = question_ids[iter2]
		a1 = getAlias(getQuestionKey(question_id1)) - m_users
		a2 = getAlias(getQuestionKey(question_id2)) - m_users
		if W[a1][a2] != 0:
			continue
		W[a1][a2] = getSimilarity(question_id1, question_id2)
		W[a2][a1] = W[a1][a2]

D = np.zeros((n_questions, n_questions))
for i in range(len(D)):
	D[i][i] = np.sum(W[i,:])


L = D - W

Z[0: m_users,0:m_users] =  np.eye(m_users)* lambda1
Z[m_users:,m_users:] = np.eye(n_questions) * lambda1 + lambda2 * L


aliased_ratings = algo(C,Z,m_users,n_questions)

ratings = dict()
for iterator in range(m_users, len(aliased_ratings)):
	assert(isQuestionKey(getId(iterator)))
	ratings[int(removeQuestionFlag(getId(iterator)))] = aliased_ratings[iterator]

computeAccuracy(ratings)
