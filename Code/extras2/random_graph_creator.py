import random

file = open('new_so_edges.txt')
vertices = {}
n_edges = 0
d = 0
for line in file:
	line = line.rstrip()
	temp = line.split(' ')
	v1 = temp[0]
	v2 = temp[1]
	vertices[v1] = True
	vertices[v2] = True
	if v1 == v2:
		d += 1
	n_edges += 1

file.close()
# print "Self loops",d

l = vertices.keys()

for i in range(n_edges):
	v1 = random.choice(l)
	v2 = random.choice(l)
	if v1 != v2:
		print v1,v2
