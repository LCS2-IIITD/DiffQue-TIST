
def checkLabel(dataset,pair):
	pair1=(pair[0],pair[1])
	pair2=(pair[1],pair[0])
	if(pair1 in dataset):
		return [True,dataset[pair1]]
	elif(pair2 in dataset):
		return [True,dataset[pair2]]
	else:
		return [False,""]

Rfile=open('new_groundtruth_Rishabh1.txt',"rb")
Afile=open('new_groundtruth_Adesh.txt',"rb")
Dfile=open('new_groundtruth_Deepak.txt',"rb")
file_domain=open('ques_pairs_with_groundtruth.txt',"rb")
merged_file=open('merged_file.txt',"wb")


Rpairs=Rfile.readlines()
Apairs=Afile.readlines()
Dpairs=Dfile.readlines()
Allpairs=file_domain.readlines()
Rdataset=dict()
Adataset=dict()
Ddataset=dict()
Alldataset=dict()

for line in Rpairs:
	temp=line.split(' ')
	# print temp
	pair=(temp[0],temp[1])
	Rdataset[pair]=temp[2]

for line in Apairs:
	temp=line.split(' ')
	pair=(temp[0],temp[1])
	Adataset[pair]=temp[2]

for line in Dpairs:
	# print line
	temp=line.split(' ')
	pair=(temp[0],temp[1])
	Ddataset[pair]=temp[2]

for line in Allpairs:
	# print line
	temp=line.split(' ')
	pair=(temp[0],temp[1])
	Alldataset[pair]=temp[2]



matched=0
rej=0
c=0
nc=0
ab=0
merged_dataset=dict()
for pair in Alldataset:
	try:
		c=c+1
		R = checkLabel(Rdataset,pair)
		A = checkLabel(Adataset,pair)
		D = checkLabel(Ddataset,pair)

		q1=pair[0]
		q2=pair[1]

		f=dict()
		f[q1]=0
		f[q2]=0
		f["X"]=0
		# print f


		Rlabel=R[1].strip()
		Alabel=A[1].strip()
		Dlabel=D[1].strip()
		# print Rlabel

		if(R[0]):
			f[Rlabel]=f[Rlabel]+1
		if(A[0]):
			f[Alabel]=f[Alabel]+1
		if(D[0]):
			f[Dlabel]=f[Dlabel]+1

		fq1=f[q1]
		fq2=f[q2]
		fx=f["X"]

		if(fq1+fq2+fx==3):
			if(fq1>=2):
				merged_dataset[pair]=q1
				matched=matched+1
			elif(fq2>=2):
				merged_dataset[pair]=q2
				matched=matched+1
				# 
			# elif(fx==1 and fq1==2):
			# 	merged_dataset[pair]=q1
			# 	matched=matched+1
			# elif(fx==1 and fq2==2):
			# 	merged_dataset[pair]=q2
			# 	matched=matched+1
			# elif(fx==2 and fq2==1):
			# 	merged_dataset[pair]=q2
			# 	matched=matched+1
			# elif(fx==2 and fq1==1):
			# 	merged_dataset[pair]=q1
			# 	matched=matched+1
				
			# elif(fx==2 and fq1==1):
			# 	merged_dataset[pair]=q1
			# 	matched=matched+1
			# elif(fx==2 and fq2==1):
			# 	merged_dataset[pair]=q2
			# 	matched=matched+1
			else:
				rej=rej+1
		else:
			ab=ab+1
		# 	merged_dataset[pair1]=q1
	except:
		nc=nc+1
print c,nc
print 'not present in all files ',str(ab)

print 'Matched by Majority ',str(matched)
print 'Rjected ',str(rej)

for i in merged_dataset:
	q1=i[0]
	q2=i[1]
	ans = merged_dataset[i]
	merged_file.write(q1+" "+q2+" "+ans+"\n")



Rfile.close()
Afile.close()
Dfile.close()
file_domain.close()
merged_file.close()		








