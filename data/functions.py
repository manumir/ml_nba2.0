import numpy as np
import pandas as pd

def process2sum(df_arg):
	train=pd.DataFrame(columns=df_arg.columns)

	j=0
	for i in set(df_arg['GameId']):
		df1=df_arg.loc[df_arg['GameId']==i]
		teams = df1['Team'].unique()
		for team in teams:
			df2=df1.loc[df1['Team']==team]
			df2=df2.reset_index(drop=True)

			for column in list(df2.columns[:4]):
				train.at[j,column]=df2.at[1,column]

			for column in list(df2.columns[4:-1]):
				train.at[j,column]=(sum(df2[column]))/len(df2[column])
			train.at[j,'Result']=df2.at[1,'Result']
			
			j=j+1
		
		print(i)
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

	# make result column be the last
	a=train['Result']
	train=train.drop(['Result','Result_away'],1)
	train['Result']=a

	return train

def myacc(preds2,test):
  preds=[]
  for i in range(len(preds2)):
    if preds2[i] < 0.5:
      preds.append(0)
    else:
      preds.append(1)

  test=list(test)
  count=0
  for i in range(len(test)):
    if preds[i]==test[i]:
      count=count+1

  return count/len(test)

def get_avgs(df1,column): 
	count=0
	try:
		for x in df1[column].values:
			count+=float(x) 
		avg=float(count/len(df1[column])) 
		return avg 
	except Exception as e: 
		print(e) 
		return np.nan

def name2acro(name):
	if name == 'Memphis Grizzlies':
		name = 'MEM'
	if name == 'Dallas Mavericks':
		name = 'DAL'
	if name == 'Indiana Pacers':
		name = 'IND'
	if name == 'Brooklyn Nets':
		name = 'BKN'
	if name == 'Atlanta Hawks':
		name = 'ATL'
	if name == 'Portland Trail Blazers':
		name = 'POR'
	if name == 'Minnesota Timberwolves':
		name = 'MIN'
	if name == 'Utah Jazz':
		name = 'UTA'
	if name == 'Chicago Bulls':
		name = 'CHI'
	if name == 'Sacramento Kings':
		name = 'SAC'
	if name == 'Toronto Raptors':
		name = 'TOR'
	if name == 'Washington Wizards':
		name = 'WAS'
	if name == 'Orlando Magic':
		name = 'ORL'
	if name == 'Denver Nuggets':
		name = 'DEN'
	if name == 'Golden State Warriors' or name == 'GS Warriors':
		name = 'GSW'
	if name == 'Phoenix Suns':
		name = 'PHX'
	if name == 'Charlotte Hornets':
		name = 'CHA'
	if name == 'Cleveland Cavaliers':
		name = 'CLE'
	if name == 'Milwaukee Bucks':
		name = 'MIL'
	if name == 'Los Angeles Clippers' or name == 'LA Clippers':
		name = 'LAC'
	if name == 'Houston Rockets':
		name = 'HOU'
	if name == 'New York Knicks' or name == 'NY Knicks':
		name = 'NYK'
	if name == 'Detroit Pistons':
		name = 'DET'
	if name == 'New Orleans Pelicans':
		name = 'NOP'
	if name == 'Philadelphia 76ers' or name == 'Philadel. 76ers':
		name = 'PHI'
	if name == 'Miami Heat':
		name = 'MIA'
	if name == 'Boston Celtics':
		name = 'BOS'
	if name == 'Oklahoma City Thunder':
		name = 'OKC'
	if name == 'San Antonio Spurs':
		name = 'SAS'
	if name == 'Los Angeles Lakers' or name == 'LA Lakers':
		name = 'LAL'
	return name
