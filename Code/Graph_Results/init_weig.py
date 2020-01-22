import xml.etree.cElementTree
import math

print "Started parsing..."
e = xml.etree.ElementTree.parse('user.xml').getroot()
e2 = xml.etree.ElementTree.parse('java_posts.xml').getroot()
print "Parsed!"

print "Stage 1"

userss = {}
maxrepu = 0
for x in e.findall('row'):
    maxrepu = max(maxrepu, int(x.get('Reputation')))

for x in e.findall('row'):
    userss[ int(x.get('Id')) ] = float(int(x.get('Reputation')))/maxrepu

print "Stage 1 over. Stage 2 started"

op = "%.8f" % ( math.exp( -userss[ 78 ] ) )
print op

kk = 0
f = open('init_edges_weight.txt','w')
for x in e2.findall('row'):
    if( x.get('ParentId') is None ):
        try:
            op = "%.8f" % ( math.exp( -userss[ int(x.get('OwnerUserId')) ] ) ) 
            op = 1 - float(op)
            op =  "%.8f" % op
            f.write(str(x.get('Id')) + " " + str(op) + "\n")
        except Exception as e:
            print x.get('OwnerUserId')
            kk += 1

print "Rej: " + str(kk)

f.close()
