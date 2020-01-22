import pickle

with open("../dump2/math_questions.dump", "rb") as fp:   # Unpickling
    math_questions = pickle.load(fp)

#print questions.keys()

from bs4 import BeautifulSoup
import re
file = open("../dump/math_posts_answers.xml")
file.readline()
fouta = open("../dump/math_posts_answers_cleaned.xml","w")
counter = 0
found = 0
not_found = 0
rejected = 0
for line in file:
    counter += 1
    if counter % 1000 == 0:
        print counter, found, rejected
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
        if parsed.row["parentid"] in math_questions:
            fouta.write(line)
            found += 1
        else:
            not_found += 1
    except:
        rejected += 1
        print "..",rejected

print counter
file.close()
fouta.close()