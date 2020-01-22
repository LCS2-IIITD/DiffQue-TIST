import matplotlib.pyplot as plt


def plot(ratings):
	list_ratings = []
	for rating in ratings.keys():
		list_ratings.append(ratings[rating])
	plt.hist(list_ratings)
	plt.title("Histogram")
	plt.xlabel("Value")
	plt.ylabel("Frequency")
	plt.show()

