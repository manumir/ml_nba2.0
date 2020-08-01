import pandas as pd
import numpy as np
import functions as f 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

train=pd.read_csv('./sumready.csv')

train = train.drop(['GameId','Team','Date','Player','GameId_away','Team_away','Date_away','Player_away'],1)

#train=pd.read_csv('./data/train_all.csv')
#train=f.process2sum(train)
#train.to_csv('sumready.csv',index=False)

#corr=train.corr()['Result']
#print(corr)

Y=train.pop('Result')
X=train

scaler = MinMaxScaler()
X = scaler.fit_transform(X)

clf=LinearRegression(n_jobs=-1)

# split data into train and test sets

#x_train,y_train = X[:-895],Y[:-895] # uncomment to
#x_test,y_test = X[-895:],Y[-895:] # test against model1 logs

x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

clf.fit(x_train,y_train)

#print(clf.score(x_test,y_test)) # gives 0.08 dk why

preds=list(clf.predict(x_test))
print(preds[:5])


f.myacc(preds,y_test)



