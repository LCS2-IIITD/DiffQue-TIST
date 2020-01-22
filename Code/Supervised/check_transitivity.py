import complete_MLP

file = open('edges.txt')

graph = {}

def addEdge(v1, v2):
	if v1 not in graph:
		graph[v1] = []
	if v2 not in graph:
		graph[v2] = []
	graph[v1].append(v2)

for line in file:
	line = line.rstrip()
	temp = line.split(' ')
	v1 = temp[0]
	v2 = temp[1]
	# assert(v1 != v2)
	addEdge(v1, v2)

file.close()

def difficulty_increasing(v1, v2):
	#Return true if v2 more difficult than v1    
	try:
		img = complete_MLP.getfeatures(int(v1), int(v2))
		label = complete_MLP.clf2.predict([img])
		if label == 1:
			return True
		else:
			return False
	except KeyError:
		return False


visited = {}

transitivity = 0
non_transitivity = 0

counter = 0
for v1 in graph:
	counter += 1
	if counter % 1000 == 0:
		print counter
		print "transitivity", transitivity,"non_transitivity", non_transitivity
	adj_list1 = graph[v1]
	for v2 in adj_list1:
		if difficulty_increasing(v1, v2) == False:
			continue
		adj_list2 = graph[v2]
		for v3 in adj_list2:
			if difficulty_increasing(v2, v3) == False:
				continue
			#Final checking. Will use this result for transitivity
			if difficulty_increasing(v1, v3):
				transitivity += 1
			else:
				non_transitivity += 1

print float(transitivity)/(transitivity + non_transitivity)
print "transitivity", transitivity,"non_transitivity", non_transitivity
