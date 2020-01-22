import random

file = open('new_so_edges.txt')
fout = open('new_so_cleaned_edges.txt','w')
edges = {}
p1 = 0; p2 = 0
for line in file:
	line = line.rstrip()
	temp = line.split(' ')
	v1 = temp[0]
	v2 = temp[1]
	if v1 == v2:
		p1 += 1
		continue
	edge = (v1, v2)
	if edge in edges:
		p2 += 1
		continue
	edges[edge] = True
	fout.write(v1 + ' ' + v2 + '\n')

fout.close()
file.close()
print p1,p2