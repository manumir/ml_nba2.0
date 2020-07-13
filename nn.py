import pandas as pd
import numpy as np
import torch
from functions import myacc
from sklearn.model_selection import train_test_split

df=pd.read_csv('train2.csv')
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
for x in set(dftrain['GameId'].values):
#for x in range(int(dftrain.tail(1)['GameId'])):
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

x_train,x_test,y_train,y_test = train_test_split(data,results,test_size=0.15, random_state=1)

print(data)
x = torch.Tensor(data)
y = torch.Tensor(results)

model = torch.nn.Sequential(
    torch.nn.Linear(320, 320),
    torch.nn.ReLU(),
    torch.nn.Linear(320,1),
)
loss_fn = torch.nn.MSELoss()

learning_rate = 1e-4
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(500):
    # Forward pass: compute predicted y by passing x to the model.
    y_pred = model(x)

    # Compute and print loss.
    loss = loss_fn(y_pred, y)
    if t % 10 == 9:
        print(t, loss.item())

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

x_test = torch.Tensor(x_test)

preds = model(x_test)
print(preds)

myacc(preds,y_test)



