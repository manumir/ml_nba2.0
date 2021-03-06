import sys
import pandas as pd

name=sys.argv[1] # name of the model, for placard 'plac'
log=pd.read_csv(name+'_log.txt')

dates=list(log['date'].values)

new=[]
for date in dates:
	year=date[-4:]
	day=date[3:5]
	month=date[:2]
	new.append(int(year+month+day))

log['date']=new

train=pd.read_csv('../data/predict.csv')

count,divider=0,0
for i in range(len(log)):
	home=log.at[i,'home']
	away=log.at[i,'away']
	date=log.at[i,'date']
	
	df=train.loc[train['date']==date]
	df=df.loc[train['team']==home]

	if len(df) > 0:
		result=round(float(df['Result'].values[0]))
		
		if name == 'plac':
			if log.at[i,'plac_A'] > log.at[i,'plac_H']:
				pred = 0
			else:
				pred = 1
		
		else:
			pred=round(float(log.at[i,'prediction']))

		if pred==result:
			count=count+1
		
		divider=divider+1
		#print('date:',date,'home:',home,'away:',away,'pred:',pred,'result:',result)

print(count/divider)
print(count,divider)

