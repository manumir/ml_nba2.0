import pandas as pd
import functions as f 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import torch

"""
new=pd.read_csv('../data/train.csv')

train=pd.DataFrame(columns=new.columns)

j=0
for i in set(new['GameId']):
	df1=new.loc[new['GameId']==i]
	teams = df1['Team'].unique()
	for team in teams:
		df2=df1.loc[df1['Team']==team]
		df2=df2.head(5)
		df2=df2.reset_index(drop=True)
		if len(df2)<5:
			print(df2)

		for column in list(df2.columns[:4]):
			train.at[j,column]=df2.at[1,column]

		for column in list(df2.columns[4:-1]):
			train.at[j,column]=sum(df2[column])
		train.at[j,'Result']=df2.at[1,'Result']

		j=j+1

	if i % 200 == 0:
		print(i)

train=train.drop(['GameId','Date','Team','Player'],1)
train=train.reset_index(drop=True)

home1,away1=[],[]
for i in range(len(train)):
  home=pd.DataFrame()
  away=pd.DataFrame()
  if i % 2 == 0:
    away1.append(i)
  else:
    home1.append(i)

away=train.loc[away1]
away=away.reset_index(drop=True)
home=train.loc[home1]
home=home.reset_index(drop=True)

train=away.join(home,rsuffix='_home')

a=train['Result']
train.pop('Result')
train.pop('Result_home')
train['Result']=a

train=train.astype(float)
print(train.corr()['Result'])

train.to_csv('sum_ready.csv',index=False)
"""

train=pd.read_csv('sum_ready.csv')

Y=train.pop('Result')
X=train

#scaler = MinMaxScaler()
#X = scaler.fit_transform(X)

clf=LinearRegression(n_jobs=-1)

# split data into train and test sets

#x_train,y_train = X[:-895],Y[:-895] # uncomment to
#x_test,y_test = X[-895:],Y[-895:] # test against model1 logs

x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

clf.fit(x_train,y_train)

#print(clf.score(x_test,y_test)) # gives 0.08 dk why

preds=list(clf.predict(x_test))
print(preds[:5])

print(f.myacc(preds,y_test))

x_train = torch.Tensor(x_train.values)
x_test = torch.Tensor(x_test.values)

y_train = torch.Tensor(y_train.values)
y_test= torch.Tensor(y_test.values)
y_train=y_train.unsqueeze(1)

model = torch.nn.Sequential(
    torch.nn.Linear(len(train.columns), len(train.columns)),
    torch.nn.Sigmoid(),
    torch.nn.Linear(len(train.columns),1),
)
loss_fn = torch.nn.MSELoss()

learning_rate = 1e-2
#optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
optimizer = torch.optim.Adagrad(model.parameters())

for t in range(1000):
	y_pred = model(x_train)
	loss = loss_fn(y_pred, y_train)
	if t % 10 == 9:
		preds = model(x_test)
		print(t, loss.item(),'train:',f.myacc(y_pred,y_train),'test:',f.myacc(preds,y_test))

	optimizer.zero_grad()

	loss.backward()

	optimizer.step()

#torch.save(model,'./12345')
