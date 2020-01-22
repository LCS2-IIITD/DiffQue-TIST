import glob

for filename in glob.glob('java_books/*.txt'):
	file = open(filename, 'r')
	print ("Reading " + filename)
	flag = True
	lines = file.readlines()
	f = ""
	for line in lines:
		f = f + line
	ending = f.find("}")
	while(ending != -1):
		starting = f[:ending].rfind("{")
		f = f[:starting] + f[ending + 1:]
		ending = f.find("}")
	file.close()
	fout = open(filename + "_cleaned", 'w')
	fout.write(f)
