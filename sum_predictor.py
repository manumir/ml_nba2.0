import pandas as pd
import numpy as np
import torch
from selenium import webdriver
from bs4 import BeautifulSoup as bs4

def checker(player):
	if player == 'Troy Brown':
		player = 'Troy Brown Jr.'

	if player == 'Lonnie Walker':
		player = 'Lonnie Walker IV'
	
	if player == 'Jaren Jackson':
		player = 'Jaren Jackson Jr.'
	
	if player == 'James Ennis':
		player = 'James Ennis III'
	
	if player == 'Danuel House':
		player = 'Danuel House Jr.'
	
	if player == 'Tim Hardaway':
		player = 'Tim Hardaway Jr.'

	if player == 'Marcus Morris':
		player = 'Marcus Morris Sr.'
	
	if player == 'Michael Porter':
		player = 'Michael Porter Jr.'
	
	if player == 'Glenn Robinson':
		player = 'Glenn Robinson III'

	return player

driver = webdriver.Firefox(executable_path='../geckodriver')

driver.get('https://www.rotowire.com/basketball/nba-lineups.php')

soup=bs4(driver.page_source,'html.parser')

driver.quit()

aways = soup.find_all('ul','lineup__list is-visit')
homes = soup.find_all('ul','lineup__list is-home')

number_of_games = len(homes)

games=list()
i=0
while i < number_of_games :
	# get list of aways players
	players=aways[i].find_all('li',class_="lineup__player")

	away=list()
	j=0
	while j < len(players):
		if len(away) == 5:
			break
		else:
			away.append(str(players[j].a['title']))
		j=j+1

	# order the list no match the training data
	A=list()
	A.append(away[2])
	A.append(away[3])
	A.append(away[4])
	A.append(away[1])
	A.append(away[0])

	# get list of home players
	players=homes[i].find_all('li',class_="lineup__player")

	home=list()
	j=0
	while j < len(players):
		if len(home) == 5:
			break
		else:
			home.append(str(players[j].a['title']))
		j=j+1
	
	# order the list no match the training data
	H=list()
	H.append(home[2])
	H.append(home[3])
	H.append(home[4])
	H.append(home[1])
	H.append(home[0])

	games.append(A+H)
	i=i+1

# get date of games
real_games=pd.read_csv('games.csv')
date=real_games['date'][0]

data= pd.read_csv('./data/train.csv')
data.pop('Result')

#model2use= input('what model to use? ')
model2use= '12345'
model= torch.load('./models/'+model2use)

file=open('./logs/'+model2use+'_log.txt','a')
for players in games:
	a=np.array([])
	df1=pd.DataFrame()
	df2=pd.DataFrame()
	i=0
	for player in players[:5]:
		if i < 5:
			player = checker(player)
			df=data.loc[data['Player']==player].tail(1)
			df1=df1.append(df)
			i=i+1
	for player in players[5:]:
			player = checker(player)
			df=data.loc[data['Player']==player].tail(1)
			df2=df2.append(df)
	
	away=str(df1.iloc[0]['Team'])#[2:-2]
	home=str(df2.iloc[0]['Team'])#[2:-2]
	
	df1=df1.drop(['GameId','Date','Team','Player'],1)
	df2=df2.drop(['GameId','Date','Team','Player'],1)

	summed_df1=pd.DataFrame()
	summed_df2=pd.DataFrame()
	for column in df1.columns:
			summed_df1.at[0,column]=sum(df1[column])
			summed_df2.at[0,column]=sum(df2[column])
	
	df=summed_df1.join(summed_df2,rsuffix='_home')
			
	a=torch.Tensor(df.values)

	file.write(home+','+away+','+date+','+str(float(model(a)))+'\n')
	print('home:',home,'away:',away,float(model(a)))

file.close()
