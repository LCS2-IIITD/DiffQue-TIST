import xml.etree.cElementTree
from datetime import datetime

e = xml.etree.ElementTree.parse('just_java.xml').getroot()

f = open('edges_time.txt', 'w')

for x in e.findall('row'):
  if( x.get('ParentId') is None and ("java" in x.get('Tags')) and ("javascript" not in x.get('Tags')) ):
      dict = {}
      
      for y in e.findall('row'):             
          if( (y.get('ParentId') is not None) and (x.get('Id') == y.get('ParentId')) ):                                                                      
              dict[y.get('OwnerUserId')] = 1 
          if( (y.get('ParentId') is not None) and (x.get('Id') == y.get('ParentId')) and (x.get('AcceptedAnswerId') is not None) and (x.get('AcceptedAnswerId')==y.get('Id'))  ):                                                                      
              dict[y.get('OwnerUserId')] = 2
              
      for y in e.findall('row'):
              ownerid = y.get('OwnerUserId')
              if( (dict.get(ownerid) is not None) and (dict.get(ownerid)==1) and (y.get('ParentId') is None) and ("java" in y.get('Tags')) and ("javascript" not in x.get('Tags')) ):
                  utc_dt1 = datetime.strptime(x.get('CreationDate'), '%Y-%m-%dT%H:%M:%S.%f')    
                  t1 = (utc_dt1 - datetime(1970, 1, 1)).total_seconds()               
                  utc_dt2 = datetime.strptime(y.get('CreationDate'), '%Y-%m-%dT%H:%M:%S.%f') 
                  t2 = (utc_dt2 - datetime(1970, 1, 1)).total_seconds()                                   
                  f.write(str(x.get('Id')) + " " + str(y.get('Id')) + " " + "0 " + str(t1) + " " + str(t2) + "\n")  
              elif( (dict.get(ownerid) is not None) and (dict.get(ownerid)==2) and (y.get('ParentId') is None) and ("java" in y.get('Tags')) and ("javascript" not in x.get('Tags')) ):
                  utc_dt1 = datetime.strptime(x.get('CreationDate'), '%Y-%m-%dT%H:%M:%S.%f')     
                  t1 = (utc_dt1 - datetime(1970, 1, 1)).total_seconds()                
                  utc_dt2 = datetime.strptime(y.get('CreationDate'), '%Y-%m-%dT%H:%M:%S.%f') 
                  t2 = (utc_dt2 - datetime(1970, 1, 1)).total_seconds()                                   
                  f.write(str(x.get('Id')) + " " + str(y.get('Id')) + " " + "1 " + str(t1) + " " + str(t2) + "\n") 