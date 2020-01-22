#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import common

s = common.getSentencesFromCorpus()

answer = "Inheritance in java is a mechanism in which one object acquires all the properties and behaviors of parent object. The idea behind inheritance in java is that you can create new classes that are built upon existing classes. When you inherit from an existing class, you can reuse methods and fields of parent class, and you can add new methods and fields also. Inheritance represents the IS-A relationship, also known as parent-child relationship. Why use inheritance? For Method Overriding (so runtime polymorphism can be achieved). For Code Reusability. Keyword extends. Types single multilevel hierarchical multiple hybrid. Inheritance in java is a mechanism in which one object acquires all the properties and behaviors of parent object."

keywords = common.getKeywordsSet(answer)
print keywords

weighted_dictionary = common.get_weighted_dictionary(answer)


keywords_found = []
keywords_found_total = []

window_size = 50
alpha = 0.5

max1 = -1
max1i = -1

total_matches = 0

for i in range(len(s)):
	if(i%10000 == 0):
		sys.stdout.write('.')
		sys.stdout.flush()
	counter = 0
	keywords_found_temp = []
	for j in range(window_size):
		if(i+j>=len(s)):
			break
		for word in s[i+j].split(" "):
			if(word in keywords and word in weighted_dictionary):
				counter = counter + weighted_dictionary[word]
				keywords_found_temp.append(word)
	if(counter > max1):
		max1i = i
		keywords_found = keywords_found_temp
	max1 = max(max1, counter)

print "\nBest match of " + str(max1) + " at " + str(max1i) + " with keywords: " + str(common.convertToDictionary(keywords_found))
threshold_minimum_score_to_qualify_as_match = alpha * max1

for i in range(len(s)):
	if(i%10000 == 0):
		sys.stdout.write('.')
		sys.stdout.flush()
	counter = 0
	keywords_found_temp = []
	for j in range(window_size):
		if(i+j>=len(s)):
			break
		for word in s[i+j].split(" "):
			if(word in keywords and word in weighted_dictionary):
				counter = counter + weighted_dictionary[word]
				keywords_found_temp.append(word)
	if(counter > threshold_minimum_score_to_qualify_as_match):
		total_matches += 1
		keywords_found_total.extend(keywords_found_temp)


print "\nTotal number of matches in second pass " + str(total_matches)
print "Words matched in total:"
print common.convertToDictionary(keywords_found_total)