#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
from imports import *

# answer = "Yes: implements Runnable is the preferred way to do it, IMO. You're not really specialising the thread's behaviour. You're just giving it something to run. That means composition is the philosophically purer way to go. In practical terms, it means you can implement Runnable and extend from another class as well."

def nlp_score(answer):
	s = common.getSentencesFromCorpus()
	keywords = common.getKeywordsSet(answer)
	# print keywords

	weighted_dictionary = common.get_weighted_dictionary(answer)


	window_size = 10
	alpha = 0.0
	beta = 0.5


	max1 = -1
	max1i = -1

	total_matches = 0.0

	k = 10
	total_lines_corpus = len(s)
	threshold = 0.8

	sentences = answer.split(".")
	sentences = [si for si in sentences if len(si) != 0 and re.search('[a-zA-Z0-9]', si)]
	for si in range(len(sentences)):
		sentences[si] = common.fix_line(sentences[si])

	maxes = []
	keywords_found_combined_sentences = []


	ans_lines_list = []
	for i in range(len(sentences)):
		ans_lines_list.append([])


	for sentence_iter in range(len(sentences)):
		########Modification for sentence level
		sentence_keywords = sentences[sentence_iter].split(" ")
		sentence_keywords = set(sentence_keywords)
		sentence_keywords = keywords.intersection(sentence_keywords)
		# print "[", sentence_iter, "]"
		###########Modification end
		max1 = -1
		keywords_found_total = []
		for i in range(len(s)):
			if(i%10000 == 0):
				# sys.stdout.write('.')
				sys.stdout.flush()
			counter = 0.0
			keywords_found_temp = []
			done = dict()
			for j in range(window_size):
				if(i+j>=len(s)):
					break
				for word in s[i+j].split(" "):
					if(word in sentence_keywords and word in weighted_dictionary):
						counter = counter + weighted_dictionary[word]
						keywords_found_temp.append(word)
						done[word] = True
			if len(done) < beta*len(sentence_keywords):
				continue
			if(len(keywords_found_temp) != 0):
				counter = counter / len(keywords_found_temp)
			if(counter > max1):
				max1i = i
			max1 = max(max1, counter)
		maxes.append(max1)
		threshold_minimum_score_to_qualify_as_match = alpha * max1
		# print ""
		present_count = 0
		for i in range(len(s)):
			if(i%10000 == 0):
				# sys.stdout.write('.')
				sys.stdout.flush()
			counter = 0.0
			keywords_found_temp = []
			done = dict()
			for j in range(window_size):
				if(i+j>=len(s)):
					break
				for word in s[i+j].split(" "):
					if(word in sentence_keywords and word in weighted_dictionary):
						counter = counter + weighted_dictionary[word]
						keywords_found_temp.append(word)
						done[word] = True
			if len(done) < beta*len(sentence_keywords):
				continue
			if(len(keywords_found_temp) != 0):
				counter = counter / len(keywords_found_temp)
			if(counter > threshold_minimum_score_to_qualify_as_match):
				present_count += 1
				ans_lines_list[sentence_iter].append(i)
				keywords_found_total.extend(keywords_found_temp)
		keywords_found_combined_sentences.extend(keywords_found_total)
		total_matches += present_count
		# print "\n",ans_lines_list[sentence_iter]
		# print sentences[sentence_iter].strip()
		# print "Best match of ", max1
		# print "Total matches of ", present_count
		# print "Words matched", common.convertToDictionary(keywords_found_total)

	# print ans_lines_list
	# print "Avg number of matches " + str(float(sum(maxes))/len(sentences))
	# print "Avg window matches " + str(total_matches/len(sentences))
	# print "Total keywords in matched windows: " + str(common.convertToDictionary(keywords_found_combined_sentences))


	temp_ans_lines_list = []
	for l in ans_lines_list:
		if l != []:
			temp_ans_lines_list.append(l)

	ans_lines_list = temp_ans_lines_list

	score = localisation.computeLocalisedScore(ans_lines_list, k, total_lines_corpus, threshold)
	return score