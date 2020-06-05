import pandas as pd

f=pd.read_csv('data2.csv')

date=list(f['Date'].values)
date2=list(f['Date2'].values)

new=[]
for x in range(len(date)):
	new.append(str(date[x])+' '+str(date2[x]))

f=f.drop(['Date2'],1)
f['Date']=new
print(f.head())
print(f.isnull().T.any().T.sum())
