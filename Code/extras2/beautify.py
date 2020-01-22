import sys
from bs4 import BeautifulSoup
fout=open('questions_for_testing.txt','w')
fin=open('temp.xml')
lines=fin.readlines()

for line in lines:
	y=BeautifulSoup(line,'xml')
	e=''
	if(y['PostTypeId']=='1'):
		e=y['Id']+" ",y['body']
		fout.write(e)


# from bs4 import BeautifulSoup
# infile = open("temp.xml","r")
# contents = infile.readlines()
# soup = BeautifulSoup(contents,'xml')
# postTypeId = soup.find_all('posttypeid')
# Id = soup.find_all('Id')
# body = soup.find_all('Body')
# print len(Id)
# for i in range(0, len(Id)):
# 	e=''
# 	print(postTypeId[i].get_text())
# 	if(postTypeId[i].get_text()=='1'):
# 		e=Id[i].get_text()+" ",body[i].get_text()
# 		fout.write(e)
    # print(titles[i].get_text(),"by",end=' ')
    # print(authors[i].get_text(),end=' ')
    # print("costs $" + prices[i].get_text())