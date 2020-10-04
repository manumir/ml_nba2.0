import pandas as pd
import numpy as np
from functions import myacc
from sklearn.model_selection import train_test_split
import xgboost as xgb

df=pd.read_csv('../data/train.csv')
df=df.drop(['FG%','FT%','3P%'],1)

"""
columns2avg=['MP','FG','FGA','FG%','3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','+/-']

train=pd.DataFrame(columns=df.columns)
j=0
for i in set(df['gameid']):
	df1=df.loc[df['gameid']==i]
	teams = df1['team'].unique()
	for team in teams:
		df2=df1.loc[df1['team']==team]
		df2=df2.reset_index(drop=True)
		df2=df2.head(7)

		for column in list(columns2avg):
			train.at[j,column]=sum(df2[column])
		train.at[j,'Result']=df2.head(1)['Result'].values[0]
		
		j=j+1
	if i % 1000 == 0:
		print(i)

train=train.drop(['gameid','date','team','player'],1)
train=train.reset_index(drop=True)

"""
train=pd.read_csv('train_summed_5_players.csv')

home1,away1=[],[]
for i in range(len(train)):
  if i % 2 == 0:
    away1.append(i)
  else:
    home1.append(i)

away=train.loc[away1]
away=away.reset_index(drop=True)
home=train.loc[home1]
home=home.reset_index(drop=True)

train=away.subtract(home)
train['Result']=away['Result']
#train=away.join(home,rsuffix='_home')
#train.pop('Result_home')

train=train.astype(float)
#print(train.corr()['Result'])

Y=train.pop('Result')
X=train
  
x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2, random_state=1)

model = xgb.XGBClassifier(n_estimators=100)
model = model.fit(x_train, y_train)

preds=model.predict(x_test)
print(preds[:5])

print(myacc(preds,y_test))

