import xml.etree.cElementTree
from datetime import datetime

e = xml.etree.ElementTree.parse('just_java.xml').getroot()

f = open('ground_truth.txt', 'w')

for x in e.findall('row'):
  if x.get('Title') is not None:
    f.write(str(x.get('Id') + "," + str(x.get('Title').encode('ascii', 'ignore'))+"\n"))
