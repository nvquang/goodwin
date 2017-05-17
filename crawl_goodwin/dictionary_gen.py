import pandas as pd
# from preprocess import *
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
import numpy
import os
import math
#from IPython.display import Image

print("Hello world")

def ngram(s, n):
	return [" ".join(s[i:i + n]) for i in range(len(s) - n + 1)]

title_list=[]

data=pd.read_csv('/home/quang/Desktop/projects/goodwin/crawl_goodwin/xxxxx.csv', error_bad_lines=False)
data=data[pd.notnull(data['job_title'])]
title_list+=data['job_title'].tolist()


#data=pd.read_csv('c_employment.csv')

#data['c_employment_job_end']=data['c_employment_job_end'].apply(lambda t: datetime.now().strftime("%Y-%m-%d") if t=='present' else t )

#data['c_employment_job_start'] = data['c_employment_job_start'].map(clean_datetime)
#data['c_employment_job_end'] = data['c_employment_job_end'].map(clean_datetime)

#data['c_employment_working']=data['c_employment_job_end']-data['c_employment_job_start']

#data['c_employment_working']=data['c_employment_working'].apply(lambda t: numpy.ceil(float(t.days)/365))
#pd.DataFrame(title_list).to_csv('title.csv')

one_gram = {}
two_gram = {}
three_gram = {}

for title in title_list:
	#print i
	#i=i+1
	
	title = ''.join(e for e in title if e.isalnum() or e == ' ')
	#title = title.replace("Sr ", "Senior ")
	title = title.split()

	for word in title:
		if word in one_gram:
			one_gram[word] += 1
		else:
			one_gram[word] = 1
	if len(title) > 1:
		for word in ngram(title, 2):
			if word in two_gram:
				two_gram[word] += 1
			else:
				two_gram[word] = 1
		if len(title) > 2:
			for word in ngram(title, 3):
				if word in three_gram:
					three_gram[word] += 1
				else:
					three_gram[word] = 1

one_gram = sorted(one_gram.items(), key = lambda x: x[1], reverse=True)
two_gram = sorted(two_gram.items(), key = lambda x: x[1], reverse=True)
three_gram = sorted(three_gram.items(), key = lambda x: x[1], reverse=True)

print("len: ", len(one_gram))
pd.DataFrame(one_gram).to_csv('one_gram.csv')
pd.DataFrame(two_gram).to_csv('two_gram.csv')
pd.DataFrame(three_gram).to_csv('trois_gram.csv')