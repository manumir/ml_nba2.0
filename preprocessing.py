import pandas as pd
import functions as f

with open('data.txt','r') as file :
	lines=file.readlines()
	print(len(lines))
	n=len(lines)
	i=0
	while i < n:
		if lines[i].find('Totals:,') > 0:
			lines.remove(lines[i])
			n=n-1
		elif lines[i].find('DNP') > 0:
			lines.remove(lines[i])
			n=n-1
		else:
			i=i+1
	print(len(lines))

new=[]
for line in lines:
	new.append(line.split(','))

df=pd.DataFrame(columns=new[0],data=new[1:])
print(df)

### join dates columns
date=list(df['Date'].values)
date2=list(df['Date2'].values)
new=[]
for x in range(len(date)):
	new.append(str(date[x])+' '+str(date2[x]))
df=df.drop(['Date2'],1)
df['Date']=new


months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Agt','Sep','Oct','Nov','Dec']
months_1=['1','2','3','4','5','6','7','8','9','10','11','12']

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

df['Team']=f.name2acro(df['Team'],'nba')
nan_rows = df[df.isnull().T.any().T]

df=df.sort_values(by=['GameId','Date'])

col=['MIN','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%','OREB','DREB','REB','AST','TOV','STL','BLK','PF','PTS','+/-']

for x in range(len(df)):
	team=df.at[x,'Team']
	player=df.at[x,'Player']
	date=df.at[x,'Date']

	df_2=df.loc[df['Team'] == team]
	df_2.reset_index(drop=True,inplace=True)
	df_2=df_2.loc[df_2['Player'] == player]
	df_2.reset_index(drop=True,inplace=True)
	df_2=df_2.loc[df_2['Date'] < date] 
	df_2.reset_index(drop=True,inplace=True)

	if len(df_2)==0:
		print(df.at[x,'Player'])
	else:
		print(df_2)


