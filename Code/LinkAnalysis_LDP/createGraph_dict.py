import pickle

def addEdge(graph,ver,neigh):
	if(ver in graph):
		l=graph[ver]
		if(neigh not in l):
			l.add(neigh)
			graph[ver] = l
			
	else:
		l=set([neigh])
		graph[ver] = l
	



graph=dict()
edges_file =  open("edges.txt","rb")
lines=edges_file.readlines()
for line in lines:
	pair=line.split(" ")
	addEdge(graph,pair[0].strip(),pair[1].strip())

with open("graph.dump","wb") as f1:
	pickle.dump(graph,f1)
# edges=[(150,300),(200,300),(100,500),(150,250),(200,250),(100,150),(250,250),(300,150),(300,250),(350,300),(150,350)]
# for i in edges:
# 	v1=i[0]
# 	v2=i[1]
# 	addEdge(graph,v1,v2)
# with open("graph_test.dump","wb") as f1:
# 	pickle.dump(graph,f1)

# print graph

