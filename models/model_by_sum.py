import pandas as pd
import functions as f 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

#train=pd.read_csv('./sumready.csv')

#train = train.drop(['GameId','Team','Date','Player','GameId_away','Team_away','Date_away','Player_away'],1)

new=pd.read_csv('../data/train.csv')

train=pd.DataFrame(columns=new.columns)

j=0
for i in range(new['GameId'].values[-1]):
  df1=new.loc[new['GameId']==i]
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

  if i % 200 == 0:
    print(i)

train=train.drop(['GameId','Date','MIN','Team','Player'],1)
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

train=train.astype(float)

print(train.corr()['Result'])


#train=f.process2sum(train)
#train.to_csv('sumready.csv',index=False)

#corr=train.corr()['Result']
#print(corr)

Y=train.pop('Result')
X=train

#scaler = MinMaxScaler()
#X = scaler.fit_transform(X)

clf=LinearRegression(n_jobs=-1)

# split data into train and test sets

#x_train,y_train = X[:-895],Y[:-895] # uncomment to
#x_test,y_test = X[-895:],Y[-895:] # test against model1 logs

x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

clf.fit(x_train,y_train)

#print(clf.score(x_test,y_test)) # gives 0.08 dk why

preds=list(clf.predict(x_test))
print(preds[:5])


print(f.myacc(preds,y_test))



