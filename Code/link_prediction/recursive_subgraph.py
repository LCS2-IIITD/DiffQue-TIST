vertices = {}
edges = []
alpha = 0.65
edges_file = open('edges.txt')
for line in edges_file:
	v1 = int(line.split(" ")[0])
	v2 = int(line.split(" ")[1])
	edges.append((v1, v2))

for e in edges:
	v1 = e[0]
	v2 = e[1]
	vertices[v1] = True
	vertices[v2] = True


def computeRanks(vertices, edges):
	#vertices: dict, edges: list
	indegree = {}
	outdegree = {}
	for v in vertices.keys():
		indegree[v] = 0
		outdegree[v] = 0
	for e in edges:
		v1 = e[0]
		v2 = e[1]
		outdegree[v1] += 1
		indegree[v2] += 1
	current_list = []
	for v in vertices.keys():
		current_list.append((indegree[v] - outdegree[v], v))
	current_list.sort(reverse = True)
	ranking = {}
	if len(current_list) < 1/alpha + 5:
		for i in range(len(current_list)):
			v = current_list[i][1]
			ranking[v] = i
		return ranking
	leaders = {}
	followers = {}
	for i in range(len(current_list)):
		v = current_list[i][1]
		if i < alpha*len(current_list):
			leaders[v] = True
		else:
			followers[v] = True
	edges_leaders = []
	edges_followers = []
	for e in edges:
		v1 = e[0]
		v2 = e[1]
		if v1 in leaders and v2 in leaders:
			edges_leaders.append(e)
		if v1 in followers and v2 in followers:
			edges_followers.append(e)
	print len(vertices), len(leaders), len(followers)
	ranking_leaders = computeRanks(leaders, edges_leaders)
	ranking_followers = computeRanks(followers, edges_followers)
	ranking = dict(ranking_leaders)
	for v in ranking_followers:
		new_rank = ranking_followers[v] + len(ranking_leaders)
		ranking[v] = new_rank
	return ranking

ranking = computeRanks(vertices, edges)

fout = open('inverse_rankings.txt', 'w')
for v in ranking:
	fout.write(str(v) + ' ' + str(len(ranking) - ranking[v]) + '\n')

fout.close()
# ranks = []
# for v in ranking.keys():
# 	ranks.append((ranking[v], v))

# ranks.sort()
# print ranks[:100]