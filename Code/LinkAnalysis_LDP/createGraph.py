import pickle

class node:
	def __init__(self,id,list):
		self.id=id
		self.list=list
def getAdjList(graph,v):
	for i in graph:
		if(i.id==v):
			return i.list

def putInAdjList(graph,v,neigh):
	for i in graph:
		if(i.id==v):
			l=i.list
			l.append(neigh)
			i.list = l
			# return l

def addEdge(graph,nodesList,ver,neigh):
	if(ver in nodesList):
		l=getAdjList(graph,ver)
		if(neigh not in l):
			putInAdjList(graph,ver,neigh)
			
	else:
		n=node(ver,[neigh])
		nodesList.append(ver)
		graph.append(n)



graph=[]
nodesList=[]
edges_file =  open("edges.txt","rb")
lines=edges_file.readlines()
for line in lines:
	pair=line.split(" ")
	addEdge(graph,nodesList,pair[0],pair[1])

with open("graph.dump","wb") as f1:
	pickle.dump(graph,f1)
# edges=[(150,300),(200,300),(100,200),(150,300),(200,250),(100,150),(250,250),(300,150),(300,250)]
# for i in edges:
# 	v1=i[0]
# 	v2=i[1]
# 	addEdge(graph,nodesList,v1,v2)

for j in graph:
	print j.id,j.list
