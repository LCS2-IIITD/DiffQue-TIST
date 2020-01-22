import sys
import pickle
from random import shuffle

with open("../question_text.dump", "rb") as fp:
	question_text = pickle.load(fp)

file = open('question_with_best_ans_and_non_best_ans_in_order.txt')
line = file.readline().strip()
file.close()

good_questions = line.split(' ')[:3000]
shuffle(good_questions)
good_questions = good_questions[:150]

pairs_done = {}
file = open('ground_truth_generated.txt')
for l in file:
	line_questions_done = l.strip().split(' ')
	pairs_done[(line_questions_done[0], line_questions_done[1])] = True
	pairs_done[(line_questions_done[1], line_questions_done[0])] = True

file.close()

print "Loading..."

potential_pairs = []
for q1 in good_questions:
	for q2 in good_questions:
		if (q1, q2) not in pairs_done and (q2, q1) not in pairs_done and (q1, q2) not in potential_pairs and (q2, q1) not in potential_pairs and q1 != q2:
			potential_pairs.append((q1, q2))

shuffle(potential_pairs)

continu = "y"
while continu == "y":
	(q1, q2) = potential_pairs.pop()
	print "1 ("+ q1 +")"
	print question_text[q1]
	print "2 ("+ q2 +")"
	print question_text[q2]
	ans = raw_input("Which is more difficult? (1/2) ")
	output = open('ground_truth_generated.txt', 'a')
	if ans == "1":
		output.write(q1 + " " + q2 + " " + q1 + "\n")
		print "Added. Thanks! xOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxO"
	elif ans == "2":
		output.write(q1 + " " + q2 + " " + q2 + "\n")
		print "Added. Thanks! xOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxOxO"
	else:
		print "Gibberish!"
	output.close()
	print "\nMore? (y/n)"
	continu = raw_input()
	if continu == "y":
		print "\n\n"

