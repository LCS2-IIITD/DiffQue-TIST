from Question import Question
import math
import random
import pickle

file_domain=open('new_so_testpairs_Deepak.txt')
#assert(False) #FIX NAME FROM RISHABH TO YOUR NAME!
new_file=open('Deepak_annotated.txt',"a+")

with open("question_text.dump", "rb") as fp:
	question_text = pickle.load(fp)

with open("old_dataset.dump", "rb") as fp1:
	old_dataset = pickle.load(fp1)

with open("new_dataset.dump", "rb") as fp2:
	new_dataset = pickle.load(fp2)

def check(pair,new_dataset):
	q1=pair[0]
	q2=pair[1]

	pair1=(q1,q2)
	pair2=(q2,q1)
	
	if(pair1 in new_dataset or pair2 in new_dataset):
		return False
	return True

i = 0
for pair in old_dataset:
	i += 1
	
	if(check(pair,new_dataset)==True):
	
		print (i)
	
		q1=pair[0]
		q2=pair[1]
		q1_text = question_text[q1]
		q2_text = question_text[q2]
	
		print (q1)
		print (q1_text)
		print ("-------------------------------------------")
		print ("")
		print (q2)
		print (q2_text)
		ans= input("Enter 1/2 : ")
	
		if(ans==1 or ans == '1'):
			# print "ADDING 1"
			new_dataset[pair]=q1
			new_file.write(q1+" "+q2+" "+q1+"\n")
		elif(ans==2 or ans == '2'):
			# print "ADDING 2"
			new_dataset[pair]=q2
			new_file.write(q1+" "+q2+" "+q2+"\n")
		else:
			new_dataset[pair]="X"
			new_file.write(q1+" "+q2+" "+"X"+"\n")
		new_file.flush()
		
		with open("new_dataset.dump", "wb") as fp:   
			pickle.dump(new_dataset, fp)
		
		print ("")
		print ("****************************************************************************************")
		print ("")
		print ("")
	else:
		print (i,"done already")

# print extended_dataset