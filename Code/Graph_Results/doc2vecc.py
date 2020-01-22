import logging
import gensim, os
import xml.etree.cElementTree
from nltk.corpus import stopwords
from string import ascii_lowercase
from collections import namedtuple
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
import pickle
import networkx as nx

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
    
dictt = {}
corpora_documents = []

e = xml.etree.ElementTree.parse('new_so_posts.xml').getroot()
for x in e.findall('row'):
    if x.get('PostTypeId') == "1":
       dictt[ x.get('Id') ] = x.get('Body') 
       corpora_documents.append( TaggedDocument(words=x.get('Body'), tags=[x.get('Id')]) )     

with open("dictidbody.dump", "wb") as fp:   #Pickling
  pickle.dump(dictt, fp)

with open("corpora_documents_save.dump", "wb") as fp:   #Pickling
  pickle.dump(corpora_documents, fp)

'''
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

        for fname in os.listdir(self.dirname):
            print fname
            for uid, line in enumerate(open(os.path.join(self.dirname, fname))):
                   sentences.append( line )
                   corpora_documents.append( TaggedDocument(words=line, tags=[uid]) )
MySentences('textll/') # a memory-friendly iterator
'''

model = Doc2Vec(size=200, min_count=1, iter=10)
model.build_vocab(corpora_documents)
model.train(corpora_documents, total_examples=len(dict), epochs=10)

model.save('mymodel2')

'''
# load the model back
model_loaded = Doc2Vec.load('mymodel2')

tokens = "a new sentence to match".split()
new_vector = model.infer_vector(tokens)
sims = model.docvecs.most_similar([new_vector]) # gives you top 10 document tags and their cosine similarity
print sims
for i in sims:
	similar=""
	print('################################')
	print i[0]
	print dictt[i[0]-1]
'''