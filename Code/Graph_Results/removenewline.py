def RemoveNewLine(oldfilename, newfilename):
	f = open(oldfilename)
	lines = f.readlines()
	f.close()
	lines[-1] = lines[-1].rstrip()
	f = open(newfilename, 'w')
	f.writelines(lines)
	f.close()

if __name__ == "__main__":
	RemoveNewLine('edges.txt', 'edges2.txt')
	
