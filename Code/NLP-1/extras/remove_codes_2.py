file = open("core_java1.txt")
flag = True
lines = file.readlines()
f = ""
for line in lines:
	f = f + line

file.close()


ending = f.find("}")
while(ending != -1):
	starting = f[:ending].rfind("{")
	if ending - starting > 50:
		print ending - starting
		print f[starting: ending]
	f = f[:starting] + f[ending + 1:]
	# print f

	ending = f.find("}")

# print f
