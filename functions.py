import numpy as np
import pandas as pd

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

  print(count/len(test))

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

def name2acro(column,site):
  teams=['BOS','BKN','NYK','PHI','TOR','CHI','CLE','DET','IND','MIL','ATL','CHA','MIA','ORL','WAS','DAL','HOU','MEM','NOP','SAS','DEN','MIN','OKC','POR','UTA','GSW','LAC','LAL','PHX','SAC']

  # name that appear on placard.com
  if site =='placard':
    teams1=['Boston Celtics','Brooklyn Nets','NY Knicks','Philadel. 76ers','Toronto Raptors',
    'Chicago Bulls','Clev. Cavaliers','Detroit Pistons','Indiana Pacers','Milwaukee Bucks',
    'Atlanta Hawks','Charl. Hornets','Miami Heat','Orlando Magic','Washin. Wizards',
    'Dall. Mavericks','Houston Rockets','Memp. Grizzlies','NO Pelicans','SA Spurs',
    'Denver Nuggets','Minnesota Timb.','OKC Thunder','Trail Blazers','Utah Jazz',
    'GS Warriors','LA Clippers','LA Lakers','Phoenix Suns','Sac. Kings']
    
  elif site=='nba':
    teams1=['Boston Celtics','Brooklyn Nets','New York Knicks','Philadelphia 76ers','Toronto Raptors',
    'Chicago Bulls','Cleveland Cavaliers','Detroit Pistons','Indiana Pacers','Milwaukee Bucks',
    'Atlanta Hawks','Charlotte Hornets','Miami Heat','Orlando Magic','Washington Wizards',
    'Dallas Mavericks','Houston Rockets','Memphis Grizzlies','New Orleans Pelicans','San Antonio Spurs',
    'Denver Nuggets','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz',
    'Golden State Warriors','LA Clippers','Los Angeles Lakers','Phoenix Suns','Sacramento Kings']
  """
  # sort teams names and teams acronyms
  teams.sort()
  teams1.sort()
  
  # bos and bkn are switched
  x=teams[1]
  teams[1]=teams[2]
  teams[2]=x
  
  # nyk and nop are switched
  x=teams[18]
  teams[18]=teams[19]
  teams[19]=x
  
  #sas and sac are switched
  x=teams[26]
  teams[26]=teams[24]
  teams[24]=x

  # por and tor are switched
  x=teams[27]
  teams[27]=teams[26]
  teams[26]=x
  """
  # names to acronyms
  new_A=[]
  for team in column:
    if team=='Philadel. ers':
      team='Philadel. 76ers'#file['away'].values:
    x=0
    for name in teams1:
      if name == team:
        name=teams[x]
        new_A.append(name)
      x=x+1
      
  return new_A
