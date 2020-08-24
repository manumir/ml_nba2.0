import pandas as pd

name=input('name of model or "plac" for plac accuracy: ')
log=pd.read_csv(name+'_log.txt')

dates=list(log['date'].values)

new=[]
for date in dates:
	year=date[-4:]
	day=date[3:5]
	month=date[:2]
	new.append(int(year+month+day))

log['date']=new

train=pd.read_csv('../data/train.csv')
train=train[-50000:]

count,divider=0,0
for i in range(len(log)):
	home=log.at[i,'home']
	away=log.at[i,'away']
	date=log.at[i,'date']
	
	df=train.loc[train['Date']==date]
	df=df.loc[train['Team']==home]

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

