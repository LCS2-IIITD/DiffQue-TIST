import xml.etree.cElementTree
import dateutil.parser as dp
from datetime import datetime

e = xml.etree.ElementTree.parse('new_so_posts.xml').getroot()

keep_time = {}
keep_accepted_ids = {}

file = open('time_diff.txt', 'w')

keep_ids = {}
q_time = []

for x in e.findall('row'):
  if x.get('PostTypeId') ==  "2":
    if x.get('Id') in keep_accepted_ids:
      first_creation_date = datetime.strptime(keep_time[x.get('Id')], '%Y-%m-%dT%H:%M:%S.%f')
      utc_dt1 = datetime.strptime(x.get('CreationDate'), '%Y-%m-%dT%H:%M:%S.%f')    
      t1 = (utc_dt1 - first_creation_date).total_seconds()               
      op = "%.8f" % ( float(t1) / (14*24*60*60) )
      file.write(str(keep_ids[x.get('Id')]) + " " + str(op) + '\n')
  else:
    if x.get('AcceptedAnswerId') is not None:
      keep_accepted_ids[x.get('AcceptedAnswerId')] = 1
      keep_time[x.get('AcceptedAnswerId')] = x.get('CreationDate')
      keep_ids[x.get('AcceptedAnswerId')] = x.get('Id')
    else:
      file.write(str(x.get('Id')) + ' 1\n')
