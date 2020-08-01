import pandas as pd

df=pd.read_csv('train1.csv')

i=2
while i < 6:
	print(i)
	df2=pd.read_csv('train'+str(i)+'.csv')
	new_ids=[]
	for j in df2['GameId'].values:
		j=j+df['GameId'].max()+1
		new_ids.append(j)
	df2['GameId']=new_ids
	df=df.append(df2)
	i=i+1

df=df.sort_values(by=['Date','GameId'])
df.to_csv('train_all.csv',index=False)

