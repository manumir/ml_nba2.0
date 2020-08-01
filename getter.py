import pandas as pd
import numpy as np
import torch


data= pd.read_csv('./data/train_all.csv')
data.pop('Result')


#players=['Jimmy Butler','Jae Crowder','Bam Adebayo','Kendrick Nunn','Duncan Robinson','Michael Porter Jr.','Paul Millsap','Nikola Jokic','Monte Morris','Torrey Craig']
players=['Joe Ingles',"Royce O'Neale",'Rudy Gobert','Donovan Mitchell','Mike Conley','Danilo Gallinari','Luguentz Dort','Steven Adams','Chris Paul','Shai Gilgeous-Alexander']
#players=['Danilo Gallinari','Luguentz Dort','Steven Adams','Chris Paul','Shai Gilgeous-Alexander','Joe Ingles',"Royce O'Neale",'Rudy Gobert','Donovan Mitchell','Mike Conley']
#players=['OG Anunoby','Pascal Siakam','Serge Ibaka','Fred VanVleet','Kyle Lowry','Danny Green','Anthony Davis','JaVale McGee','Kentavious Caldwell-Pope','LeBron James']
#players=['Victor Oladipo','T.J. Warren','Myles Turner','Aaron Holiday','Malcolm Brogdon','Tobias Harris','Ben Simmons','Joel Embiid','Josh Richardson','Shake Milton']

a=np.array([])
df1=pd.DataFrame()
for player in players:
	df=data.loc[data['Player']==player].tail(1)
	df1=df1.append(df)

print(df1)
df1=df1[df1.columns[4:]]

for ar in df1.values:
	ar=np.array(ar)
	a=np.concatenate((a,ar))

a=torch.Tensor(a)
model= torch.load('lineups_model')

print(model(a))
