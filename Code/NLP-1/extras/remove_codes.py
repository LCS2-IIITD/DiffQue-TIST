file = open("temp.txt")
flag = True
lines = file.readlines()

output = []

while flag:
	found = False
	flag = False
	last_open = -1
	last_line = ""
	last_line_partial = ""
	for line in lines:
		if found == False:
			ret = line.find("{")
			if ret == -1:
				output.append(line)
			else:
				# output.append(line[:ret])
				found = True
				flag = True
				last_line_partial = line[:ret]
				last_line = line
		elif found == True:
			ret = line.find("}")
			if ret == -1:
				pass
			else:
				output.append(line[ret + 1:])
				found = False
	lines = output
	for line in lines:
		print line

file.close()
print lines