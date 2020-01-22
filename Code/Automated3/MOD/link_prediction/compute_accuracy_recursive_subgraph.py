from common2 import computeAccuracy
f = open('inverse_rankings.txt')
ratings = {}
for line in f:
	question_id = int(line.split(" ")[0])
	value = float(line.split(" ")[1])
	ratings[question_id] = value

f.close()
computeAccuracy(ratings)
