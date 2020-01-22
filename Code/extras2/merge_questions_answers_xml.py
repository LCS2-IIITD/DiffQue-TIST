from bs4 import BeautifulSoup

d = dict()

file = open('../dump/java_posts_questions.xml')
counter = 0
for line in file:
	counter += 1
	if counter % 1000 == 0:
		print counter
	parsed = BeautifulSoup(line, "lxml")
	d[int(parsed.row["id"])] = line

file.close()

file = open('../dump/java_posts_answers.xml')
counter = 0
for line in file:
	counter += 1
	if counter % 1000 == 0:
		print counter
	parsed = BeautifulSoup(line, "lxml")
	d[int(parsed.row["id"])] = line

file.close()

ids = d.keys()
ids.sort()

fout = open('java_posts.xml',"w")
counter = 0
for key in ids:
	counter += 1
	if counter % 1000 == 0:
		print counter
	fout.write(d[key])

fout.close()