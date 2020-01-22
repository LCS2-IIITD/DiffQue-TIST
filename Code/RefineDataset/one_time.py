from Question import Question
# import common2
# from common2 import *
import math
import random
import pickle

old_file=open('new_so_testpairs_Deepak.txt')
#assert(False) #FIX NAME FROM RISHABH TO YOUR NAME!
new_file=open('Deepak_annotated.txt',"a+")

with open("new_so_questions4.dump", "rb") as fp:   # Unpickling
	questions = pickle.load(fp)
	
question_text = dict()

for q in questions:
	question_text[q] = questions[q].question_text

with open("question_text.dump", "wb") as fp1:   #Pickling
	pickle.dump(question_text, fp1)

old_pairs=old_file.readlines()
new_pairs=new_file.readlines()

old_dataset=[]

for line in old_pairs:
	temp=line.rstrip().split(' ')
	pair=(temp[0],temp[1])
	old_dataset.append(pair)

with open("old_dataset.dump", "wb") as fp1:   #Pickling
	pickle.dump(old_dataset, fp1)

new_dataset=dict()

for line in new_pairs:
	temp=line.rstrip().split(' ')
	pair=(temp[0],temp[1])
	new_dataset[pair] = temp[2]
	print (pair)

with open("new_dataset.dump", "wb") as fp2:   #Pickling
	pickle.dump(new_dataset, fp2)

new_file.close()
old_file.close()