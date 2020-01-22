from scipy import stats
import numpy as np
from math import sqrt
from scipy.stats import norm

#each element of list would indicate how many times second question was more difficult than the first in the survey
#sample list for 20 questions:
#random_survey_results = [9,8,11,10,12]
#proposed_survey_results = [18,15,16,19,18,20,19,13]
# H0: mu = 10 or mu = total_questions/2
# H1: mu > 10 or mu > total_questions/2
def compute(total_questions, random_survey_results = [], proposed_survey_results = [], alpha = 0.05):
	sample_std = np.std(proposed_survey_results, ddof = 1) #ddof = 1 ensured the denominator while calculating variance is n - 1
	sample_mean = np.mean(proposed_survey_results)
	mean = np.mean(random_survey_results)
	std = np.std(random_survey_results, ddof = 1) #estimating the population mean
	print "population stats","mean",mean,"std",std
	print "sample stats","sample_mean",sample_mean,"sample_std", sample_std
	#The below is used when population std is NOT known
	T = sqrt(len(proposed_survey_results)) * (sample_mean - total_questions/2)
	T = T/sample_std
	t = stats.t.ppf(1 - alpha, len(proposed_survey_results) - 1)
	print "significance level",alpha
	print "T = ",T,"t =",t
	if T <= t:
		print "Bad luck. Our technique is not significant by one-sided t-test. Null hypothesis NOT rejected."
	else:
		print "Good! Our technique is significant by one-sided t-test! Null hypothesis rejected."
	#The below is used when population std is known. For our purpose we are computing it from the sample itself.
	Z = (sqrt(len(proposed_survey_results))/std)*(sample_mean - total_questions/2)
	z = stats.norm.ppf(1 - alpha)
	p = 1 - norm.cdf(Z)
	print "Z = ",Z,"z =",z, "p-value = ",p
	if Z <= z:
		print "Bad luck. Our technique is not significant when population std computed from sample. Null hypothesis NOT rejected."
	else:
		print "Good! Our technique is significant when population std computed from sample! Null hypothesis rejected."


if __name__ == "__main__":
	random_survey_results = [12,11,11,10,12,8,9,10,13]
	proposed_survey_results = [15,16,15,16,8,16,16,18]
	compute(20, random_survey_results, proposed_survey_results, alpha = 0.05)