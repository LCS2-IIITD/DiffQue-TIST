def binarySearch(list,x,low,high):

	if len(list) == 0:
		return -1
	if(x <= list[low]):
		return low; 
 
	if(x > list[high]):
		return -1
 
	mid = (low + high)/2
 
	if(list[mid] == x):
		return mid

	elif(list[mid] < x):
		if(mid + 1 <= high and x < list[mid+1]):
			return mid + 1
		else:
			return binarySearch(list,x, mid+1, high)
	else:
		if(mid - 1 >= low and x > list[mid-1]):
			return mid
		else:    
			return binarySearch(list,x ,low, mid - 1)



# list=[3,7,11,12,15,19]
# print list
# for x in range(0,21):
# 	i=binarySearch(list,x,0,len(list)-1)
# 	if(i>=0):
# 		print x,' ',list[i]
# 	else:
# 		print i