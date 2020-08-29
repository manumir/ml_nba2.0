import pandas as pd
import numpy as np
import functions as f
import time

df=pd.read_csv('all_data.txt')
#df=pd.read_csv('data19-20.txt')
df.pop('drop_this')

print(df)

del2=[]
for x in range(len(df)):
	if df.at[x,'MIN']=='-'or df.at[x,'Player']=='Totals: - - -' or df.at[x,'MIN']=='DNP':
		del2.append(x)
df=df.drop(del2)
df=df.reset_index(drop=True)

### turn date column to int for compairson
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
months_1=['01','02','03','04','05','06','07','08','09','10','11','12']

dates=list(df['Date'].values)
new=[]
for x in range(len(df)):
	date=str(dates[x])
	date=date.split(' ')
	if len(date[1])==1:
		date[1]='0'+date[1]
	for name in months:
		if date[0] == name:
			ix=months.index(name)
			new.append(int(date[2]+months_1[ix]+date[1]))

df['Date']=new

# make a game id column
x,i=0,0
ids=[]
count=0
while x < len(df):
  home=df.at[x,'Team']    
  date=df.at[x,'Date']

  df_2=df.loc[df['Date'] == date]
  df_2=df_2.loc[df_2['Team'] == home]

  x=df_2.tail(1).index[0]+1
  i=i+0.5
  
  count=count+len(df_2)
  if i % 1 == 0:
    for j in range(count):
      ids.append(int(i))
    count=0
df['GameId']=ids

### make a result column
x,i=0,0
new=[]
while x < len(df):
	team=df.at[x,'Team']
	date=df.at[x,'Date']

	df_2=df.loc[df['Date'] == date]
	df_2=df_2.loc[df_2['Team'] == team]
	df_3=df_2.loc[df_2['Player']=='Totals:']

	if int(df_3['PTS'].values[0]) > 0:
		for x in range(len(df_2)):
			if i%2==0:
				new.append(1)
			else:
				new.append(0)
	else:
		for x in range(len(df_2)):
			if i%2==0:
				new.append(0)
			else:
				new.append(1)

	i=i+1
	x=df_2.tail(1).index[0]+1
df['Result']=new

# delete lines that have the totals of each team and players that DNP (did not play)
del2=[]
for x in range(len(df)):
	if df.at[x,'Player'] == 'Totals:':
		del2.append(x)
df=df.drop(del2)
df.reset_index(drop=True,inplace=True)

# change MIN column to int
new=[]
for x in range(len(df)):
	a=df.at[x,'MIN']
	a=int(a[:a.find(':')])
	b=df.at[x,'MIN']
	b=int(b[b.find(':')+1:])
	new.append(((a*60)+b)/60)
df['MIN']=new

### change team names to acronimo
new=[]
for team in df['Team']:
	new.append(f.name2acro(team))
df['Team']=new

### check for nan rows
nan_rows = df[df.isnull().T.any().T]
print(nan_rows)

## sort by date and game id
df=df.sort_values(by=['Date','GameId'])

## columns to average
cols=['MIN','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%','OREB','DREB','REB','AST','TOV','STL','BLK','PF','PTS','+/-']

start=time.time()
og=df.copy()
for x in range(len(df)):
	team=df.at[x,'Team']
	player=df.at[x,'Player']
	date=df.at[x,'Date']

	df_2=og.loc[og['Player'] == player]
	df_2.reset_index(drop=True,inplace=True)

	df_2=df_2.loc[df_2['Date'] < date]
	df_2.reset_index(drop=True,inplace=True)

	df_2=df_2.loc[df_2['Team'] == team]
	df_2.reset_index(drop=True,inplace=True)

	df_2=df_2.tail(10)

	if len(df_2) > 0:
		for col in cols:
			y=0
			for value in df_2[col]:
				if value == '-': # doesn't work
					value = 0 # idk why
				y=y+float(value)

			avg=y/len(df_2)
			df.at[x,col]=avg
	if x % 1024 == 0:
		print(x)

print(time.time()-start)
print(df)

# removing the '-' where it should be zero
cols=['FG%','3P%','FT%']
for x in range(len(df)):
	for col in cols:
		if df.at[x,col]=='-':
			df.at[x,col]=0

df.to_csv('just2predict.csv',index=False)

