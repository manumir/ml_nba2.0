import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

df=pd.read_csv('train.csv')

train=pd.DataFrame(columns=df.columns)

j=0
for i in range(df['GameId'].values[-1]):
	df1=df.loc[df['GameId']==i]
	teams = df1['Team'].unique()
	for team in teams:
		df2=df1.loc[df1['Team']==team]
		df2=df2.reset_index(drop=True)

		for column in list(df2.columns[:4]):
			train.at[j,column]=df2.at[1,column]

		for column in list(df2.columns[4:-1]):
			train.at[j,column]=sum(df2[column])
		train.at[j,'Result']=df2.at[1,'Result']
		
		j=j+1
	
	print(i)

train=train.drop(['GameId','Date','MIN','Team'],1)
train.pop('Player')
train=train.reset_index(drop=True)

home1,away1=[],[]
for i in range(len(train)):
	home=pd.DataFrame()
	away=pd.DataFrame()
	if i % 2 == 0:
		home1.append(i)
	else:
		away1.append(i)

home=train.loc[home1]
home=home.reset_index(drop=True)
away=train.loc[away1]
away=away.reset_index(drop=True)

train=home.join(away,rsuffix='_away')

a=train['Result']
train.pop('Result')
train.pop('Result_away')
train['Result']=a

#print(train['Team'],'\n',train['Team_away'])
scaler = MinMaxScaler()
train= pd.DataFrame(scaler.fit_transform(train), columns=train.columns)

clf=LinearRegression(n_jobs=-1)

# split data into train and test sets
Y=train.pop('Result')
X=train
x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
clf.fit(x_train,y_train)

#print(clf.score(x_test,y_test)) # gives 0.08 dk why


preds2=list(clf.predict(x_test))
print(preds2[:5])

preds=[]
for i in range(len(preds2)):
	if preds2[i] < 0.5:
		preds.append(0)
	else:
		preds.append(1)
		
y_test=list(y_test)
count=0
for i in range(len(y_test)):
	if preds[i]==y_test[i]:
		count=count+1

print(count/len(y_test))



