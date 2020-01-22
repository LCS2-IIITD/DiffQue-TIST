class Queue(object):
    def __init__(self, queue=None):
        if queue is None:
            self.queue = []
        else:
            self.queue = list(queue)
    def dequeue(self):
        return self.queue.pop(0)
    def enqueue(self, element):
        self.queue.append(element)
    def empty(self):
    	if(len(self.queue)==0):
    		return True
    	return False




# def dfs(graph,u, d, visited, path,len2):
# 	print "doing",str(u)
# 	visited[u]= True
# 	path.append(u)

# 	if u == d:
# 		return path
# 		# allpaths.append(path)
# 		# print allpaths
# 	# elif u not in graph:
# 	# 	return []
# 	else:
# 		allpaths=[]
# 		l=getAdjList(graph,u)
# 		for i in l:
# 			if i in visited :
# 				if visited[i]==False:
# 					print allpaths
# 					allpaths+=extend(dfs(graph,i,d,visited, path,len2))
# 			else:
# 				allpaths+=(dfs(graph,i,d,visited, path,len2))

# 	return allpaths

# 	path.pop()
# 	visited[u]= False

def dfs2(graph,start, end, path):
    # print "...",str(nodesList)
    path = path + [start]
    # print 'adding ',str(start)
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    l=graph[start]

    for node in l:
        if node not in path:
            paths.extend(dfs2(graphnode, end, path))
    print 'returning ', str(paths)
    return paths

# graph=[]
# nodesList=[]
# edges=[(150,300),(200,300),(100,200),(150,300),(200,250),(100,150),(250,250),(300,150),(300,250)]
# for i in edges:
# 	v1=i[0]
# 	v2=i[1]
# 	addEdge(graph,nodesList,v1,v2)

# for j in graph:
# 	print j.id,j.list

# print nodesList
with open("graph.dump","rb") as f1:
	graph = pickle.load(f1)

test_file = open("merged.txt","rb")
lines=test_file.readlines()
for line in lines:
	temp=line.split(" ")
	path=[]
	src=temp[0]
	ddest=temp[1]
	p=dfs2(graph,src,dest,path)
	path2=0
	path3=0
	for i in p:
		if(len(i)==3):
			path2=path2+1
		elif(len(i)==4):
			path3=path3+1
	print path2,path3
	break


# path=[]

# p=dfs2(graph,nodesList,100,250,path)
# print p
# path2=0
# path3=0
# for i in p:
# 	if(len(i)==3):
# 		path2=path2+1
# 	elif(len(i)==4):
# 		path3=path3+1
# print path2,path3
# print allpaths




