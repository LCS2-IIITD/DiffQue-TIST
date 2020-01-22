from bs4 import BeautifulSoup

fin = open("../dump/math_posts.xml")
foutq = open("../dump/math_posts_questions.xml", "w")
fouta = open("../dump/math_posts_answers.xml", "w")
counter = 0
rejected = 0
for line in fin:
	counter += 1
	if counter % 1000 == 0:
		print counter
	try:
		parsed = BeautifulSoup(line)
		if parsed.row["posttypeid"] == "1":
			foutq.write(line)
		if parsed.row["posttypeid"] == "2":
			fouta.write(line)
	except:
		rejected += 1
		print "..",rejected


foutq.close()
fouta.close()
fin.close()