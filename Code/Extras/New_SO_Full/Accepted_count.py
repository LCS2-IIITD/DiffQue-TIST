import xml.etree.cElementTree
import dateutil.parser as dp

e = xml.etree.ElementTree.parse('new_so_posts.xml').getroot()

user_rating_map = {}
accepted_id = {}
fl = open('ans_count.txt', 'w')

for x in e.findall('row'):
  if x.get('PostTypeId') ==  "2":
    if x.get('Id') in accepted_id:
      if x.get('OwnerUserId') in user_rating_map:
        user_rating_map[x.get('OwnerUserId')] += 1
      else:
        user_rating_map[x.get('OwnerUserId')] = 1
  elif x.get('PostTypeId') == "1":
    if x.get('OwnerUserId') in user_rating_map:   
       fl.write(str(x.get('Id')) + " " + str(user_rating_map[x.get('OwnerUserId')]) + '\n')
    else:
       fl.write(str(x.get('Id')) + " " + "0" + '\n') 
    if x.get('AcceptedAnswerId') is not None:
      accepted_id[x.get('AcceptedAnswerId')] = 1
      #print x.get('Id'), x.get('AcceptedAnswerId')
