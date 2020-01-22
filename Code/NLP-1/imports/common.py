#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import math
from textblob import TextBlob as tb
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import glob
import collections
import operator

stops = set(stopwords.words("english"))
lmtzr = WordNetLemmatizer()

line_grouping_threshold = 1

def getSentencesFromCorpus():
	global s
	return s

def getKeywordsSet(answer):
	keywords = []
	temp_tokens = [w for w in fix_line(answer).split(" ") if not w in stops]
	keywords = keywords + temp_tokens
	keywords = set(keywords)
	return keywords

def fix_line(line):
	line = line.lower()
	line = re.sub(r"[^ a-zA-Z\n]"," ",line)
	line = line.replace("\n"," ")
	words = line.split(" ")
	words = [w for w in words if not w in stops]
	line_words = []
	for word in words:
		if(len(word)>0):
			noun_lmtzr = lmtzr.lemmatize(word,'n').encode('ascii')
			verb_lmtzr = lmtzr.lemmatize(word,'v').encode('ascii')
			if(len(word)!= len(noun_lmtzr)):
				line_words.append(noun_lmtzr)
			else:
				line_words.append(verb_lmtzr)
	line_words = [w for w in line_words if not w in stops]
	line = ' '.join(line_words)
	return line.strip()

def tf(word, blob):
	return blob.words.count(word) / float(len(blob.words))

def n_containing(word, bloblist):
	return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
	return math.log(float(len(bloblist)) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
	return tf(word, blob) * idf(word, bloblist)

def get_weighted_dictionary(answer):
	global bloblist
	# print ("Building dictionary")
	bloblist = [tb(fix_line(answer))] + bloblist
	weighted_dictionary = compute_weighted_dictionary(bloblist)
	# print ("Dictionary built")
	return weighted_dictionary



def compute_weighted_dictionary(bloblist):
	weighted_dictionary = {}
	for i, blob in enumerate(bloblist):
		# print("Top words in document {}".format(i + 1))
		scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
		sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
		for word, score in sorted_words[:20]:
			# print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
			weighted_dictionary[word] = round(score, 5)
		break
	# print weighted_dictionary
	return weighted_dictionary

def convertToDictionary(items):
	counts = dict()
	for i in items:
		counts[i] = counts.get(i, 0) + 1
	return counts

s = []
bloblist = []
for filename in glob.glob('java_books/*.txt'):
	fin = open(filename, 'r')
	# if(filename.find("core_java") == -1):
	# 	fin.close()
	# 	continue
	print ("Reading " + filename)

	line_counter = 0
	fixed_lines_bloblist = []
	for line in fin.readlines():
		fixed_line = fix_line(line)
		if(re.search('[a-zA-Z]', fixed_line)):
			line_counter += 1
			fixed_lines_bloblist.append(fixed_line)
			s.append(fixed_line)
			if(line_counter == line_grouping_threshold):
				bloblist.append(' '.join(fixed_lines_bloblist))
				line_counter = 0
				fixed_lines_bloblist = []
	bloblist.append(' '.join(fixed_lines_bloblist))
	fin.close()
print ("Corpus read completely")

# bloblist = []
# fin = open('stackoverflow_corpus/corpusSO20k.txt', "r")
# for line in fin:
# 	line = fix_line(line)
# 	bloblist = bloblist + [tb(line)]
# fin.close()

# print ("Import finished")

