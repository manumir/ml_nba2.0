import pandas as pd
import numpy as np
import functions as f

df=pd.read_csv('data.txt')
df=df[:4009]
print(df.tail())
### join dates columns
date=list(df['Date'].values)
date2=list(df['Date2'].values)
new=[]
for x in range(len(date)):
	new.append(str(date[x])+' '+str(date2[x]))
df=df.drop(['Date2'],1)
df['Date']=new
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Agt','Sep','Oct','Nov','Dec']
months_1=['01','02','03','04','05','06','07','08','09','10','11','12']
new=[]
for x in range(len(df)):
	date=df.at[x,'Date'].split(' ')
	if len(date[1])==1:
		date[1]='0'+date[1]
	for name in months:
		if date[0] == name:
			ix=months.index(name)
			new.append(int(date[2]+months_1[ix]+date[1]))
df['Date']=new

### make a result column
x=0
new=[]
while x < len(df):
	team=df.at[x,'Team']
	date=df.at[x,'Date']

	df_2=df.loc[df['Team'] == team]
	df_2=df_2.loc[df_2['Date'] == date]
	df_3=df_2.loc[df_2['Player']=='Totals:']

	if int(df_3['PTS'].values[0]) > 0:
		for x in range(len(df_2)):
			new.append(1)
	else:
		for x in range(len(df_2)):
			new.append(0)

	x=df_2.tail(1).index[0]+1
df['Result']=new

# delete lines that have the totals of each team and players that DNP (did not play)
del2=[]
for x in range(len(df)):
	if df.at[x,'Player'] == 'Totals:' or df.at[x,'MIN']=='DNP':
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
df['Team']=f.name2acro(df['Team'],'nba')

### check for nan rows
nan_rows = df[df.isnull().T.any().T]

## sort by date and game id
df=df.sort_values(by=['Date','GameId'])

## columns to average
cols=['MIN','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%','OREB','DREB','REB','AST','TOV','STL','BLK','PF','PTS','+/-']

og=df.copy()
print(df.loc[df['Player']=='Ersan Ilyasova'])
for x in range(len(df)):
	team=df.at[x,'Team']
	player=df.at[x,'Player']
	date=df.at[x,'Date']

	df_2=og.loc[og['Team'] == team]
	df_2.reset_index(drop=True,inplace=True)
	
	df_2=df_2.loc[df_2['Date'] < date]
	df_2.reset_index(drop=True,inplace=True)

	df_2=df_2.loc[df_2['Player'] == player]
	df_2.reset_index(drop=True,inplace=True)
	
	df_2=df_2.tail(10)

	if len(df_2) > 0:
		for col in cols:
			y=0
			for value in df_2[col]:
				y=y+float(value)
			avg=y/len(df_2)
			
			df.at[x,col]=avg
		if df.at[x,'Player']=='Isaiah Canaan':
			print(df_2)
	print(x)

print(df)
print(og.loc[og['Player']=='Ersan Ilyasova'])
print(df.loc[df['Player']=='Ersan Ilyasova'])

