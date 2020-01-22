#
#	RUN SCRIPT IN TWO PARTS. CONTACT PANDEY SIR!
#	THIS SCRIPT SHOULDN'T BE REQUIRED. THIS IS ALREADY ADDED TO MSR COMBINED SCRIPT
#

fin = open('edges_msr.txt')
fout = open('edges_msr_correct.txt', 'w')
old_name_to_new_name = dict()
new_name_to_old_name = dict()
next_free_id = 1
for line in fin:
	v1 = line.strip().rstrip().split(" ")[0]
	v2 = line.strip().rstrip().split(" ")[1]
	if v1 not in old_name_to_new_name:
		old_name_to_new_name[v1] = str(next_free_id)
		new_name_to_old_name[str(next_free_id)] = v1
		next_free_id += 1
	if v2 not in old_name_to_new_name:
		old_name_to_new_name[v2] = str(next_free_id)
		new_name_to_old_name[str(next_free_id)] = v2
		next_free_id += 1
	fout.write(str(old_name_to_new_name[v1]) + ' ' + str(old_name_to_new_name[v2]) + '\n')

fout.close()
fin.close()


fin = open('rank_nodes_pagerank_without_weight.txt')
fout = open('rank_nodes_pagerank_without_weight2.txt', 'w')
for line in fin:
	v = line.strip().rstrip().split(" ")[0]
	value = line.strip().rstrip().split(" ")[1]
	if new_name_to_old_name[v].startswith("q"):
		fout.write(new_name_to_old_name[v][1:] + " " + value + '\n')

fout.close()
fin.close()