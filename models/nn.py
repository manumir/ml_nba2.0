import pandas as pd
import numpy as np
import torch
from functions import myacc
from sklearn.model_selection import train_test_split

df=pd.read_csv('../data/train.csv')
#df=df.drop(['FG%','3P%','FT%'],1)

ix=[] 
for i in set(df['GameId'].values):
	df1=df.loc[df['GameId']==i]
	teams = df1['Team'].unique()
	for team in teams:
		for index in list(df1.loc[df1['Team']==team][:5].index):
			ix.append(index)

dftrain=df.loc[ix]
data=[]
results=[]
for x in set(dftrain['GameId'].values):
	dftrain1=dftrain[df.columns[4:]]
	dftrain1=dftrain1.astype('float')
	dftrain1=dftrain1.loc[dftrain['GameId']==x]
	result=list(dftrain1.pop('Result'))

	ar=np.array([])
	for array in dftrain1.values:
		array=np.array(array)
		ar=np.concatenate((ar,array))
	data.append(ar)
	results.append(result[0])
	
	if x % 1024 == 0:
		print(x)

data=np.array(data)
results=np.array(results)

np.save('x',data)
np.save('y',results)

ar=np.zeros(200)

x_train,x_test,y_train,y_test = train_test_split(data,results,test_size=0.2, random_state=1)

x_train = torch.Tensor(x_train)
x_test = torch.Tensor(x_test)

y_train = torch.Tensor(y_train)
y_test= torch.Tensor(y_test)
y_train=y_train.unsqueeze(1)

model = torch.nn.Sequential(
    torch.nn.Linear(len(ar), len(ar)),
    torch.nn.Sigmoid(),
    torch.nn.Linear(len(ar),1),
)
loss_fn = torch.nn.MSELoss()

learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for t in range(5000):
	y_pred = model(x_train)
	loss = loss_fn(y_pred, y_train)
	if t % 10 == 9:
		preds = model(x_test)
		print(t, loss.item(),'train:',myacc(y_pred,y_train),'test:',myacc(preds,y_test))

	optimizer.zero_grad()

	loss.backward()

	optimizer.step()

#torch.save(model,'./12345')
print(preds[:5])


