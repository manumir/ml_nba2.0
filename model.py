import pandas as pd
import numpy as np
from functions import myacc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier

df=pd.read_csv('train.csv')
ix=[]
for i in range(df['GameId'].values[-1]):
    df1=df.loc[df['GameId']==i]
    df1=df1.sort_values(by=['MIN'],ascending=False)
    teams = df1['Team'].unique()
    for team in teams:
        for index in list(df1.loc[df1['Team']==team][:8].index):
            ix.append(index)

dftrain=df.loc[ix]
data=[]
results=[]
for x in range(int(dftrain.tail(1)['GameId'])):
	dftrain1=dftrain[df.columns[4:]]
	dftrain1=dftrain1.loc[dftrain['GameId']==x]
	result=list(dftrain1.pop('Result'))
	#print(dftrain1,result[0])

	ar=np.array([])
	for array in dftrain1.values:
			ar=np.concatenate((ar,array))
	data.append(ar)
	#data.append(result[0])
	results.append(result[0])

x_train,x_test,y_train,y_test = train_test_split(data,results,test_size=0.1, random_state=1)

clf=LinearRegression(n_jobs=-1)
#clf=MLPClassifier(activation='logistic',solver='adam',random_state=1,max_iter=10000)

#x_train,x_test,y_train,y_test = train_test_split(data[::2],data[1::2], test_size=0.2, random_state=1)

#x_train,x_test,y_train,y_test = data[:1000:2],data[1002::2],data[1:1001:2],data[1003::2]

clf.fit(x_train,y_train)

#print(clf.score(data[1002::2],data[1003::2]))

preds=list(clf.predict(x_test))
print(preds[:5])

myacc(preds,y_test)

