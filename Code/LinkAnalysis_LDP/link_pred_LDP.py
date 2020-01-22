import pickle

def dfs3(graph,start, end, path,depth):
    # print "...",str(nodesList)
    
    # path = path + [start]
    # print 'adding ',str(start),
    # print ".",
    if(depth<=0):
        return []
    if start == end:
        # assert(False)
        return [path]
    if start not in graph:
        return []
    paths = []
    path[start]=True
    l=graph[start]
    # print path
    # assert(len(path)<=depth)
    for node in l:
        if node not in path:
            paths.extend(dfs3(graph,node, end, path,depth-1))

    del path[start]
    # print 'returning ', str(paths)
    return paths


# def dfs2(graph,start, end, path,depth):
#     # print "...",str(nodesList)
#     path = path + [start]
#     # print 'adding ',str(start),
#     # print ".",
#     if(depth<=0):
#     	return []
#     if start == end:
#         return [path]
#     if start not in graph:
#         return []
#     paths = []
#     l=graph[start]
#     # print len(l)

#     for node in l:
#         if node not in path:
#             paths.extend(dfs2(graph,node, end, path,depth-1))

#     path.remove(start)
#     # print 'returning ', str(paths)
#     return paths





with open("graph.dump","rb") as f1:
	graph = pickle.load(f1)



test_file = open("merged_file.txt","rb")
lines=test_file.readlines()
for line in lines:
	temp=line.split(" ")
	path=dict()
	src=temp[0]
	dest=temp[1]
	depth=8
	path2=0
	path3=0
	print src,dest
	p=dfs3(graph,src,dest,path,depth+1)
	print len(p)
	for i in p:
		if(len(i)==3):
			path2=path2+1
		elif(len(i)==4):
			path3=path3+1
	print path2,path3
	# break





