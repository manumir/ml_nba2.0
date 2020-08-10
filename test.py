#import functions as f

"""
teams1=['Boston Celtics','Brooklyn Nets','New York Knicks','Philadelphia 76ers','Toronto Raptors',
'Chicago Bulls','Cleveland Cavaliers','Detroit Pistons','Indiana Pacers','Milwaukee Bucks',
'Atlanta Hawks','Charlotte Hornets','Miami Heat','Orlando Magic','Washington Wizards',
'Dallas Mavericks','Houston Rockets','Memphis Grizzlies','New Orleans Pelicans','San Antonio Spurs',
'Denver Nuggets','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz',
'Golden State Warriors','LA Clippers','Los Angeles Lakers','Phoenix Suns','Sacramento Kings']

l=[]
for x in teams1:
	l2=[]
	l2.append(x)
	print(l2,'==',f.name2acro(l2,'nba'))
	l.append(l2)
"""
import pandas as pd
import numpy as np
import torch

model2use=input('model to use? ')
model=torch.load(model2use)

df=pd.read_csv('./data/train.csv')

ix=[] 
for i in set(df['GameId'].values):
	df1=df.loc[df['GameId']==i]
#	df1=df1.sort_values(by=['MIN'],ascending=False)
	teams = df1['Team'].unique()
	for team in teams:
		for index in list(df1.loc[df1['Team']==team][:5].index):
			ix.append(index)

dftrain=df.loc[ix]
#data=[]
#results=[]
count=0
for x in set(dftrain['GameId'].values):
#for x in range(int(dftrain.tail(1)['GameId'])):

	dftrain1=dftrain[df.columns[4:]]
	dftrain1=dftrain1.astype('float')
	dftrain1=dftrain1.loc[dftrain['GameId']==x]
	dftrain2=dftrain.loc[dftrain['GameId']==x]
	result=list(dftrain1.pop('Result'))

	away=str(dftrain2.head(1)['Team'].values)[1:-1]
	home=str(dftrain2.tail(1)['Team'].values)[1:-1]
	date=str(dftrain2.tail(1)['Date'].values)[1:-1]
	
	ar=np.array([])
	for array in dftrain1.values:
		array=np.array(array)
		ar=np.concatenate((ar,array))
#	data.append(ar)
#	results.append(result[0])

	food=torch.Tensor(ar)
	#print(model(food),round(float(model(food))))
	#print('x:',x,'date:',date,'home:',home,'away:',away,'proj:',model(food),'result:',result[0])

	if round(float((model(food)))) == int(result[0]):
		count=count+1

print(count)
print(count/len(set(dftrain['GameId'].values)))


