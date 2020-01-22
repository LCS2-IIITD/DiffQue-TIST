import pickle

math_questions = dict()


#print questions.keys()

from bs4 import BeautifulSoup
import re
file = open("../dump/math_posts_questions.xml")
file.readline()
fouta = open("../dump/math_posts_questions_cleaned.xml","w")
counter = 0
found = 0
not_found = 0
rejected = 0
t1 = 0; t2 = 0; t3 = 0; t4 = 0;
for line in file:
    counter += 1
    if counter % 1000 == 0:
        print counter, found, rejected, t1, t2, t3, t4
    line = line.replace("&lt;p&gt;","")
    line = line.replace("&lt;/p&gt;","")

    line = line.replace("&lt;li&gt;","")
    line = line.replace("&lt;/li&gt;","")

    line = line.replace("&lt;ul&gt;","")
    line = line.replace("&lt;/ul&gt;","")

    line = line.replace("&#xA;","")
    line = line.replace("&#xD;","")

    line = line.replace("&quot;","")
    line = line.replace("&lt;","")
    line = line.replace("&gt;","")
    line = line.replace("&amp;","")
    try:
        parsed = BeautifulSoup(line)
        tags = parsed.row["tags"]
        if "probability" in tags :
            fouta.write(line)
            found += 1
            t1 += 1
            math_questions[parsed.row["id"]] = True
        elif "combinatorics" in tags:
            fouta.write(line)
            found += 1
            t2 += 1
            math_questions[parsed.row["id"]] = True
        elif "inclusion" in tags and "exclusion" in tags:
            fouta.write(line)
            found += 1
            t3 += 1
            math_questions[parsed.row["id"]] = True
        elif "permutations" in tags:
            fouta.write(line)
            found += 1
            t4 += 1
            math_questions[parsed.row["id"]] = True
        else:
            not_found += 1
    except:
        rejected += 1
        print "Rejected",rejected

print counter
file.close()
fouta.close()
with open("../dump2/math_questions.dump", "wb") as fp:   #Pickling
    pickle.dump(math_questions, fp)