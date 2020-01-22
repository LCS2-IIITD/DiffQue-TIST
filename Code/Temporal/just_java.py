import xml.etree.cElementTree
import re

filee = open('just_java.xml', 'w')

dict = {}
with open('stackoverflow_top.xml') as f:
    for line in f.readlines():
        #line = str(line)
        line = str(re.sub('\s+',' ',line))
        x = xml.etree.ElementTree.fromstring(line)
        if (x is not None) and (x.get('Tags') is not None): 
            if ("java" in x.get('Tags')) and ("javascript" not in x.get('Tags')):
                  dict[x.get('Id')] = 1


with open('stackoverflow_top.xml') as f:
    for line in f.readlines():
        #line = str(line)
        line = str(re.sub('\s+',' ',line))
        x = xml.etree.ElementTree.fromstring(line)
        if x is not None: 
            if (x.get('Id') in dict) or ( (x.get('ParentId') is not None) and (x.get('ParentId') in dict) ):
                filee.write(line+'\n')
               
filee.close()