import random

file = open('new_so_edges.txt')
edges = {}
n_edges = 0
d = 0
for line in file:
	line = line.rstrip()
	temp = line.split(' ')
	v1 = temp[0]
	v2 = temp[1]
	if v1 != v2:
		edges[(v1, v2)] = True

file.close()

file = open('new_so_user_edges.txt')
for line in file:
	line = line.rstrip()
	temp = line.split(' ')
	v1 = temp[0]
	v2 = temp[1]
	assert(v1 != v2)
	if v1 != v2:
		if (v1,v2) in edges:
			del edges[(v1,v2)]

fout_back_edges = open('new_so_back_edges.txt','w')
fout_forward_edges = open('new_so_forward_edges.txt','w')

for e in edges:
	v1 = e[0]
	v2 = e[1]
	assert(v1 != v2)
	if int(v1) > int(v2):
		fout_back_edges.write(v1 + ' ' + v2 + '\n')
	else:
		fout_forward_edges.write(v1 + ' ' + v2 + '\n')

fout_back_edges.close()
fout_forward_edges.close()