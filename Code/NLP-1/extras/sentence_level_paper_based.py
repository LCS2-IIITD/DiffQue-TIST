#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import common
import re
from compute_similarity import similarity

s = common.getSentencesFromCorpus()

answer = "Encapsulation is a strategy used as part of abstraction. Encapsulation refers to the state of objects - objects encapsulate their state and hide it from the outside; outside users of the class interact with it through its methods, but cannot access the classes state directly. So the class abstracts away the implementation details related to its state. Abstraction is a more generic term, it can also be achieved by (amongst others) subclassing. For example, the interface List in the standard library is an abstraction for a sequence of items, indexed by their position, concrete examples of a List are an ArrayList or a LinkedList. Code that interacts with a List abstracts over the detail of which kind of a list it is using. Abstraction is often not possible without hiding underlying state by encapsulation - if a class exposes its internal state, it can't change its inner workings, and thus cannot be abstracted. Abstraction is the concept of describing something in simpler terms, i.e abstracting away the details, in order to focus on what is important (This is also seen in abstract art, for example, where the artist focuses on the building blocks of images, such as colour or shapes). The same idea translates to OOP by using an inheritance hierarchy, where more abstract concepts are at the top and more concrete ideas, at the bottom, build upon their abstractions. At its most abstract level there is no implementation details at all and perhaps very few commonalities, which are added as the abstraction decreases. As an example, at the top might be an interface with a single method, then the next level, provides several abstract classes, which may or may not fill in some of the details about the top level, but branches by adding their own abstract methods, then for each of these abstract classes are concrete classes providing implementations of all the remaining methods. Encapsulation is a technique. It may or may not be for aiding in abstraction, but it is certainly about information hiding and/or organisation. It demands data and functions be grouped in some way - of course good OOP practice demands that they should be grouped by abstraction. However, there are other uses which just aid in maintainability etc."

window_size = 10
max1 = -1
max1i = -1

total_matches = 0.0

sentences = answer.split(".")
sentences = [si for si in sentences if len(si) != 0 and re.search('[a-zA-Z0-9]', si)]
for si in range(len(sentences)):
	sentences[si] = common.fix_line(sentences[si])

for sentence_iter in range(0, len(sentences), window_size):
	max_score = -1
	for i in range(len(s)):
		# if(i%100 == 0):
			# sys.stdout.write('.')
			# sys.stdout.flush()
		print i
		lines = ""
		for j in range(window_size):
			if(i+j>=len(s)):
				break
			lines = lines + s[i + j]
		score = similarity(sentences[sentence_iter] ,lines, False)
		max_score = max(max_score, score)
		print score
	print sentences[sentence_iter]
	print max_score


