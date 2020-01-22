edges_file = open('edges.txt')
graph = []
for line in edges_file:
	v1 = int(line.split(" ")[0])
	v2 = int(line.split(" ")[1])
	graph.append((v1, v2))


ratings_file = open('rank_nodes_pagerank_without_weight.txt')
ratings = {}
for line in ratings_file:
	question_id = int(line.split(" ")[0])
	value = float(line.split(" ")[1])
	ratings[question_id] = value


#Graph Analysis:
adj_list = dict()
for e in graph:
	v1 = e[0]
	v2 = e[1]
	adj_list[v1] = []
	adj_list[v2] = []

for e in graph:
	v1 = e[0]
	v2 = e[1]
	adj_list[v1].append(v2)
	adj_list[v2].append(v1)

visited = {}

def BFSAndAnalyze(v, root, depth, parent):
	global counts_analyzer, visited
	if depth > 10 or v in visited:
		return [0, 0]
	visited[v] = ratings[v]
	local_more_less = [0, 0]
	if ratings[v] < ratings[root]:
		local_more_less[1] = 1
	else:
		local_more_less[0] = 1
	for neighbour in adj_list[v]:
		if neighbour > root and neighbour > v:
			local_local_more_less = BFSAndAnalyze(neighbour, root, depth + 1, v)
			local_more_less[0] += local_local_more_less[0]
			local_more_less[1] += local_local_more_less[1]
	return local_more_less



more_less = [0, 0]
counter = 0
for v in adj_list.keys():
	counter += 1
	counts_analyzer = 0
	visited = {}
	local_more_less = BFSAndAnalyze(v, v, 0, -1)
	more_less[0] += local_more_less[0]
	more_less[1] += local_more_less[1]
	if counter % 100 == 0:
		print counter, float(more_less[1])/(more_less[0] + more_less[1])

print "Total more_less", more_less
