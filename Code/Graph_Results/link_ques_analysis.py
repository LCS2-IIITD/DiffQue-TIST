from Question import Question
import pickle
def func(str1,ans_to_ques):
	start=0
	end=len(str1)
	indexes=[]
	links=[]
	links_ques=[]
	# Find start indexes of all links
	i=str1.find("http://stackoverflow.com/",start,end)
	while(i!=-1):
		indexes.append(i)
		start=i+1
		i=str1.find("http://stackoverflow.com/",start,end)
	if(len(indexes)>0):
		# If some indexes found ... extract all links
		for i in indexes:
			space=str1.find(" ",i,len(str1))
			link=str1[i:space]
			links.append(link)

		# extract ques_id in links
		for link in links:
			if(link.find("http://stackoverflow.com/a/",0,len(link)) != -1):
				p=0
				ans=[int(s) for s in link.split("/") if s.isdigit()]
				ans=set(ans)
				for j in ans:
					if(ans[j] in ans_to_ques):
						q = ans_to_ques[ans[j]]
						links_ques.append(q)
			elif(link.find("http://stackoverflow.com/questions/",0,len(link)) != -1):
				q=[int(s) for s in link.split("/") if s.isdigit()] #  of the form q=[[456]]  so q[0] in next line
				links_ques.append(str(q[0]))
			else:
				
				continue

	return links_ques


with open("questions4.dump", "rb") as fp:
	questions = pickle.load(fp)


with open("answer_texts_by_question_id4.dump", "rb") as fp1:
	ques_answers = pickle.load(fp1)

with open("answer_questionid4.dump", "rb") as fp2:
	ans_to_ques = pickle.load(fp2)

file1=open("Links_analysis_edges_BothSide.txt","wb")


qlist=[]

for ques in questions:
	ques_id = questions[ques].question_id
	qlist.append(ques_id)


f=0 #rejected
a=0 #analysed
l=0 # finlly questions having links
links_edges=[]
for ques in questions:
	ques_id = questions[ques].question_id
	try:
		answers = ques_answers[ques_id]
		for ans in answers:
			links_ques_ids = func(ans,ans_to_ques)
			if(len(links_ques_ids)>0):
				l=l+1
				for i in links_ques_ids:
					if(str(i) in qlist and str(i)!=ques_id):

						links_edges.append([str(i),str(ques_id)])
						links_edges.append([str(ques_id),str(i)])

						file1.write(str(i)+" "+ques_id+"\n")
						file1.write(ques_id+" "+str(i)+"\n")

		a=a+1
	
	except:
		f=f+1
# print links_edges

with open("Links_analysis_edges_BothSide.dump", "wb") as fp3:
	pickle.dump(links_edges,fp3)
print "-----------------"
print f
print a
print len(links_edges)
# print c
file1.close()
