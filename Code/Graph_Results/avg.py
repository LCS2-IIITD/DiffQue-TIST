import xml.etree.cElementTree
import dateutil.parser as dp
from datetime import datetime

e = xml.etree.ElementTree.parse('java_posts.xml').getroot()

keep_time = {}
seconddict = {}
keep_ids = {}
q_time = []

for x in e.findall('row'):
  if x.get('PostTypeId') ==  "2":
    if ( x.get('ParentId') is not None ) and ( int(x.get('Score'))>0 or (x.get('AcceptedAnswerId') is not None) ) and ( x.get('ParentId') in keep_time ):
      first_creation_date = datetime.strptime(keep_time[x.get('ParentId')], '%Y-%m-%dT%H:%M:%S.%f')
      utc_dt1 = datetime.strptime(x.get('CreationDate'), '%Y-%m-%dT%H:%M:%S.%f')    
      t1 = (utc_dt1 - first_creation_date).total_seconds()               
      op = "%.8f" % ( float(t1) / 60 )
      seconddict[ x.get('ParentId') ] = op    
  else:
      keep_time[x.get('Id')] = x.get('CreationDate')
    
ans = 0
for key, value in seconddict.items():
    ans += float(value)

print(ans)
print(len(seconddict))
print( ans/len(seconddict) )

hh = ans/len(seconddict)
hh /= 60
hh /= 24
print( hh )
