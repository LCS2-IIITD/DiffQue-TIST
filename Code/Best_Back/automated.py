import os
import shutil

filename = "edges_new_1.txt"

try:
    os.remove("page_rank/" + filename)
except OSError:
    pass
try:
    os.remove("page_rank/" + "edges.txt")
except OSError:
    pass

shutil.copy2("backsize/" + filename, "page_rank/")
os.rename("page_rank/" + filename, "page_rank/" + "edges.txt")

os.chdir("page_rank/")
print(os.getcwd())
filee = open("edges.txt", "r")
lines = filee.readlines()
lines = lines[:-1]

fout = open('edges.txt','w')
for line in lines:
  fout.write(line)
'''
os.system("npm start")
'''