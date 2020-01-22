from common2 import computeAccuracy
from random import randint
from sys import argv


def computeAccuracyFromJSOutput(filename):
	f = open(filename)
	ratings = {}
	for line in f:
		question_id = int(line.split(" ")[0])
		value = float(line.split(" ")[1])
		ratings[question_id] = value
	f.close()
	computeAccuracy(ratings)

if __name__ == "__main__":
	f = None
	if len(argv) == 1:
		f = open('rank_nodes_pagerank_without_weight.txt')
	else:
		f = open('rank_nodes_pagerank_without_weight' + argv[1] + '.txt')
		print "Special mode entered. Contact AP if this is not intentional"
		print "Reading",'rank_nodes_pagerank_without_weight' + argv[1] + '.txt'

	ratings = {}
	for line in f:
		question_id = int(line.split(" ")[0])
		value = float(line.split(" ")[1])
		ratings[question_id] = value

	f.close()
	computeAccuracy(ratings)

