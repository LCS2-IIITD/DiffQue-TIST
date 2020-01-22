#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import common
import re

s = common.getSentencesFromCorpus()

answer = "Abstract class can have abstract and non-abstract methods.	Interface can have only abstract methods. Since Java 8, it can have default and static methods also. Abstract class doesn't support multiple inheritance.	Interface supports multiple inheritance. Abstract class can have final, non-final, static and non-static variables.	Interface has only static and final variables. Abstract class can provide the implementation of interface.	Interface can't provide the implementation of abstract class. The abstract keyword is used to declare abstract class. The interface keyword is used to declare interface.Methods of a Java interface are implicitly abstract and cannot have implementations. A Java abstract class can have instance methods that implements a default behaviour. Variables declared in a Java interface are by default final. An abstract class may contain non-final variables. Members of a Java interface are public by default. A Java abstract class can have the usual flavours of class members like private, protected, etc. A Java interface should be implemented using keyword “implements”; A Java abstract class should be extended using keyword “extends”. An interface can extend another Java interface only, an abstract class can extend another Java class and implement multiple Java interfaces. A Java class can implement multiple interfaces but it can extend only one abstract class."

keywords = common.getKeywordsSet(answer)
print keywords

weighted_dictionary = common.get_weighted_dictionary(answer)


window_size = 10
beta = 0.8

total_matches = 0.0

sentences = answer.split(".")
sentences = [si for si in sentences if len(si) != 0 and re.search('[a-zA-Z0-9]', si)]
for si in range(len(sentences)):
	sentences[si] = common.fix_line(sentences[si])

keywords_found_combined_sentences = []

for sentence_iter in range(len(sentences)):
	########Modification for sentence level
	sentence_keywords = sentences[sentence_iter].split(" ")
	sentence_keywords = set(sentence_keywords)
	sentence_keywords = keywords.intersection(sentence_keywords)
	print "[", sentence_iter, "]"
	###########Modification end
	keywords_found_total = []
	present_count = 0
	for i in range(len(s)):
		if(i%10000 == 0):
			sys.stdout.write('.')
			sys.stdout.flush()
		counter = 0.0
		keywords_found_temp = []
		verify_dict = dict()
		for j in range(window_size):
			if(i+j>=len(s)):
				break
			for word in s[i+j].split(" "):
				if(word in sentence_keywords and word in weighted_dictionary):
					counter = counter + weighted_dictionary[word]
					keywords_found_temp.append(word)
					verify_dict[word] = True
		if(len(verify_dict) >= beta*len(sentence_keywords)):
			present_count += 1
			keywords_found_total.extend(keywords_found_temp)
	keywords_found_combined_sentences.extend(keywords_found_total)
	total_matches += present_count
	print "\n", sentences[sentence_iter].strip()
	print "Total matches of ", present_count
	print "Words matched", common.convertToDictionary(keywords_found_total)

print "Avg window matches " + str(total_matches/len(sentences))
print "Total keywords in matched windows: " + str(common.convertToDictionary(keywords_found_combined_sentences))
