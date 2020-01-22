from __future__ import division
from BS_floorValue import binarySearch
import math

infinity = 10**9


class occ_node:
	def __init__ (self,b):
		self.lines=b

def sortFunc(a):
	return a

def prevIndexOfLine(occ_list, line_no, ans_line_no):
	if ans_line_no in occ_list[line_no].lines:
		return line_no
	return -1

def removeLineOccurence(occ_list,line_no,ans_line_no):
	temp_list=occ_list[line_no].lines
	if(line_no==-1):
		return
	else:
		if(len(temp_list)!=0 and ans_line_no in temp_list):
			occ_list[line_no].lines.remove(ans_line_no)
			
def addLineOccurrence(occ_list,ans_line_no,index):
	if(ans_line_no not in occ_list[index].lines):
		occ_list[index].lines.append(ans_line_no)
		
def findLargest(queue):
	max=-2000
	ind=0
	for i in range(0,len(queue)):
		if(queue[i]>max):
			max=queue[i]
			ind=i
	return ind
def  findSmallest(queue):
	min=1000000
	ind=0
	for i in range(0,len(queue)):
		if(queue[i]<min):
			min=queue[i]
			ind=i
	return ind

def addToQueue(queue,cost,k):
	queue.append(cost)
	n=len(queue)
	if(n>k):
		larg = findLargest(queue)
		queue.remove(queue[larg])
	
def showOccList(l):
	for i in l:
		k=1
		# print i.lines,


def removeJunkQueue(queue):
	q = []
	for element in queue:
		if element != infinity:
			q.append(element)
	return q

def computeVariance(results):
	m = sum(results) / len(results)
	varRes = sum([(xi - m)**2 for xi in results]) / len(results)
	# print "Variance is",varRes

def computeLocalisedScore(ans_lines_list, k, total_lines_corpus, threshold):
	
	threshold_no_of_lines=int(math.ceil(threshold*len(ans_lines_list)))
	queue=[]
	occ_list=[]  
	current_list=[]    # to store the latest occurrence of answer lines ---- length= no of lines in answer
	for i in range(0,total_lines_corpus):
		occ_list.append(occ_node([]))
	# print "Computing localization score"
	for line_no in range(0,total_lines_corpus):#total_lines_corpus+1):
		current_list = []
		for ans_line_no in range(0,len(ans_lines_list)):
			temp_list=ans_lines_list[ans_line_no]
			removeLineOccurence(occ_list,line_no-1,ans_line_no)
			index=binarySearch(temp_list,line_no,0,len(temp_list)-1)
			if(index>=0):
				lineNoAtIndex=temp_list[index]
				addLineOccurrence(occ_list,ans_line_no,lineNoAtIndex)
				current_list.append(lineNoAtIndex)
		current_list.sort(reverse=False,key=sortFunc)
		if(threshold_no_of_lines<=len(current_list)):
			x=current_list[threshold_no_of_lines-1]
			cost = x-line_no+1
			addToQueue(queue,cost,k)
			# if cost < 10:
				# print cost, line_no
		else:
			addToQueue(queue, infinity, k)
	queue = removeJunkQueue(queue)
	queue.sort()
	# print queue
	if len(queue) != 0:
		mean = float(sum(queue))/len(queue)
		var = computeVariance(queue)
		return mean
	else:
		# print "Cannot compute mean and variance"
		return -1
	# print queue[findSmallest(queue)]

if __name__ == "__main__":
	ans_lines_list=[[3,7,11,12,15,19],[2,4,17],[10,20],[5,9,10,12],[5,11,12]]
	# ans_lines_list=[[2,5],[3,6],[11,12]]
	# ans_lines_list=[[4,8],[6,7],[1,2]]
	# ans_lines_list = [[]]
	k=6
	total_lines_corpus = 21
	threshold=0.8
	computeLocalisedScore(ans_lines_list, k, total_lines_corpus, threshold)