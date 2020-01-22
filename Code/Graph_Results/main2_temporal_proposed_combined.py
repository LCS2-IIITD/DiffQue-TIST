from Question import Question
import pagerank
from common2 import *
import xml.etree.cElementTree
from datetime import datetime
from trueskill import *
from compute_accuracy_from_js_output import computeAccuracyFromJSOutput

x = -1

print "Started parsing..."
if dataset == "old":
    e = xml.etree.ElementTree.parse('old_so_posts.xml').getroot()
elif dataset == "math":
    e = xml.etree.ElementTree.parse('math_posts.xml').getroot()
elif dataset == "new":
    e = xml.etree.ElementTree.parse('new_so_posts.xml').getroot()
elif dataset == "mid":
    e = xml.etree.ElementTree.parse('mid_so_posts.xml').getroot()
else:
    assert(False)

print "Parsed!"

#Part1
idd = -1
temporal_questionid = []
listli = []
print "Starting stage 1"

# Hardcoded respective xmls
if dataset == "old":
    first_creation_date = datetime.strptime("2008-08-01T16:08:52.353", '%Y-%m-%dT%H:%M:%S.%f') 
    last_creation_date = datetime.strptime("2010-12-08T20:30:21.590", '%Y-%m-%dT%H:%M:%S.%f')
elif dataset == "math":
    first_creation_date = datetime.strptime("2010-07-20T19:22:12.190", '%Y-%m-%dT%H:%M:%S.%f') 
    last_creation_date = datetime.strptime("2017-08-27T03:45:54.667", '%Y-%m-%dT%H:%M:%S.%f')
elif dataset == "new":
    first_creation_date = datetime.strptime("2015-08-01T00:03:00.543", '%Y-%m-%dT%H:%M:%S.%f') 
    last_creation_date = datetime.strptime("2017-08-27T04:23:44.787", '%Y-%m-%dT%H:%M:%S.%f')
elif dataset == "mid":
    first_creation_date = datetime.strptime("2012-01-01T00:24:23.940", '%Y-%m-%dT%H:%M:%S.%f') 
    last_creation_date = datetime.strptime("2013-12-31T23:55:25.333", '%Y-%m-%dT%H:%M:%S.%f')
else:
    assert(False)

bucket_count = (last_creation_date - first_creation_date).days
bucket_count = int(bucket_count/14)
print "bucket_count", bucket_count
print "number of users", len(user_questions)

for i in range(bucket_count + 1):
  temporal_questionid.append([])

for x in e.findall('row'):
    if( x.get('ParentId') is None ):
        utc_dt1 = datetime.strptime(x.get('CreationDate'), '%Y-%m-%dT%H:%M:%S.%f')    
        t1 = (utc_dt1 - first_creation_date).days
        t1 = int(t1/14)
        temporal_questionid[t1].append(x.get('Id'))

question_times = {}
for i in range(len(temporal_questionid)):
    for question_id in temporal_questionid[i]:
        question_times[question_id] = i


print "Stage 1 over. Stage 2 started"

# Part 2
# user_questions[ownerid] = list of his question ids

graph = []
counter = 0
rejected = 0
edges_dict = {}
user_edge_count = 0
forward_edge_count = 0
back_edge_count = 0
freeze_forward_backward_edges = False

def addEdge(e):
    if e not in edges_dict:
        if e[0] == e[1]:
            return
        if e[0] == x or e[1] == x:
            return
        edges_dict[e] = True
        graph.append(e)

def printEdgeCounts():
    global user_edge_count, forward_edge_count, back_edge_count, freeze_forward_backward_edges
    if freeze_forward_backward_edges is False:
        forward_edge_count = 0
        back_edge_count = 0
        for e in edges_dict:
            v1 = str(e[0])
            v2 = str(e[1])
            if question_times[v1] > question_times[v2]:
                back_edge_count += 1
            else:
                forward_edge_count += 1
    print "forward_edge_count", forward_edge_count, "back_edge_count", back_edge_count, "user_edge_count", user_edge_count




for i in range(len(temporal_questionid)-1):
    counter += 1
    print counter,"/",len(temporal_questionid) - 1, rejected
    printEdgeCounts()
    possible_ids = temporal_questionid[i] + temporal_questionid[i + 1]
    for question_id in possible_ids:
        try:
            post = questions[question_id]
        except KeyError:
            rejected += 1
            # print question_id
            continue
        for non_best_user in post.non_best_answer_user_ids:
            try:
                for question2 in user_questions[non_best_user]:
                    if(question2 in possible_ids):
                        addEdge((int(question_id), int(question2)))
            except KeyError:
                pass
        try:
            for question2 in user_questions[post.best_answer_user_id]:
                if(question2 in possible_ids):
                    addEdge((int(question_id), int(question2)))
        except KeyError:
            pass
    possible_ids = temporal_questionid[i] 
    possible_ids2 = temporal_questionid[i + 2:]
    possible_ids2 = [item for sublist in possible_ids2 for item in sublist]
    for question_id in possible_ids:
        try:
            post = questions[question_id]
        except KeyError:
            rejected += 1
            # print question_id
            continue
        for non_best_user in post.non_best_answer_user_ids:
            try:
                for question2 in user_questions[non_best_user]:
                    if(question2 in possible_ids2):
                        addEdge((int(question_id), int(question2)))
            except KeyError:
                pass
        try:
            for question2 in user_questions[post.best_answer_user_id]:
                if(question2 in possible_ids2):
                    addEdge((int(question_id), int(question2)))
        except KeyError:
            pass

printEdgeCounts()
freeze_forward_backward_edges = True

counter = 0
for user in user_questions.keys(): #iterate over the users
  counter += 1
  if counter % 1000 == 0:
    print counter,"/",len(user_questions)
    printEdgeCounts()
  uquestions = user_questions[user]
  user_temporal_questionid = {}
  for i in range(len(temporal_questionid)):
    user_temporal_questionid[i] = []
  for i in range(len(uquestions)):
    qtime = question_times[uquestions[i]]
    # if qtime not in user_temporal_questionid:
    #   user_temporal_questionid[qtime] = []
    user_temporal_questionid[qtime].append(uquestions[i])
  for t in range(0, max(user_temporal_questionid.keys())):
    next_time = t + 1
    while next_time < len(user_temporal_questionid) and len(user_temporal_questionid[next_time]) == 0:
      next_time += 1
    for q1 in user_temporal_questionid[t]:
      if next_time < len(user_temporal_questionid):
        for q2 in user_temporal_questionid[next_time]:
          addEdge((int(q1), int(q2)))
          user_edge_count += 1
  # for i in range(len(uquestions) - 1):
  #   graph.append((uquestions[i], uquestions[i + 1]))

printEdgeCounts()


print "Processing for PageRank"

filename = 'edges_temporal_' + dataset + '.txt'
rank_file = 'temporal_'+dataset+'_ranks.txt'

print "Writing edges for PageRank as",filename
f = open(filename,'w')
for edge in graph:
  f.write(str(edge[0]) + " " + str(edge[1]) + "\n")

f.close()

RemoveNewLine(filename, filename)

print "Processing npm"

system('rm '+ rank_file)
system("cp " + filename + ' Temporal/page_rank/')
system('cd Temporal/page_rank && npm start ' + filename + ' '+ rank_file + '&& cp ' + rank_file +' ../../')

print "Computing final rank for PageRank"

computeAccuracyFromJSOutput(rank_file)




# HITS

print "Processing for HITS"
G=nx.Graph()

for edge in graph:
    G.add_edge(*edge)

h,a=hits_nx(G)

difficulty = dict()
for i in questions.keys():
    if(h.has_key(int(i))):
        difficulty[int(i)] = h[int(i)]
    else:
        difficulty[int(i)]=0

print "Computing accuracy for HITS"
computeAccuracy(difficulty)

#TRUESKILL
print "Processing for trueskill"
ratings = dict()
for e in graph:
    v1 = e[0]
    v2 = e[1]
    ratings[v1] = Rating()
    ratings[v2] = Rating()

edges_dict2 = {}
counter = 0
for (v1, v2) in graph:
    counter += 1
    if counter % 1000 == 0:
        print counter
    if (v1, v2) not in edges_dict2:
        ratings[v2], ratings[v1] = rate_1vs1(ratings[v2], ratings[v1])
        edges_dict2[(v1, v2)] = True

for rating in ratings:
    ratings[rating] = ratings[rating].mu

print "Computing accuracy for trueskill"
computeAccuracy(ratings)



