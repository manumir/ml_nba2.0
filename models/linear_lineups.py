import pandas as pd
import numpy as np
from functions import myacc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df=pd.read_csv('../data/train.csv')
df=df.drop(['FG%','FT%','3P%'],1)

ix=[]
for i in range(df['GameId'].values[-1]):
  df1=df.loc[df['GameId']==i]
  df1=df1.sort_values(by=['MIN'],ascending=False)
  teams = df1['Team'].unique()
  for team in teams:
    for index in list(df1.loc[df1['Team']==team][:5].index):
      ix.append(index)

dftrain=df.loc[ix]
data=[]
results=[]
for x in set(dftrain['GameId'].values):
#for x in range(int(dftrain.tail(1)['GameId']))
	if x % 200 == 0:
		print(x)
	dftrain1=dftrain[df.columns[4:]]
	dftrain1=dftrain1.astype('float')
	dftrain1=dftrain1.loc[dftrain['GameId']==x]
	result=list(dftrain1.pop('Result'))
	#print(dftrain1,result[0])

	ar=np.array([])
	for array in dftrain1.values:
			ar=np.concatenate((ar,array))
	data.append(ar)
	#data.append(result[0])
	results.append(result[0])
  
x_train,x_test,y_train,y_test = train_test_split(data,results,test_size=0.2, random_state=1)

clf=LinearRegression(n_jobs=-1)

clf.fit(x_train,y_train)

preds=clf.predict(x_test)

print(myacc(preds,y_test))

