import pandas as pd
import numpy as np
import torch
from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4
import re

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

	return player


driver = webdriver.Firefox(executable_path='../geckodriver')

driver.get('https://www.rotowire.com/basketball/nba-lineups.php')
#WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'lineup__player')))

soup=bs4(driver.page_source,'html.parser')

driver.quit()

homes = soup.find_all('ul','lineup__list is-visit')
aways= soup.find_all('ul','lineup__list is-home')

number_of_games = len(homes)

games=list()
i=0
while i < number_of_games :
	# get list of aways players
	players=homes[i].find_all('li',class_="lineup__player")

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
	players=aways[i].find_all('li',class_="lineup__player")

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

	games.append(H+A)
	games.append(A+H)
	i=i+1

data= pd.read_csv('./data/train_all.csv')
data.pop('Result')

for players in games:
	a=np.array([])
	df1=pd.DataFrame()
	for player in players:
		player = checker(player)
		df=data.loc[data['Player']==player].tail(1)
		df1=df1.append(df)
	
	away=str(df1.head(1)['Team'].values)[1:-1]
	home=str(df1.tail(1)['Team'].values)[1:-1]

	df1=df1[df1.columns[4:]]

	for ar in df1.values:
		ar=np.array(ar)
		a=np.concatenate((a,ar))

	a=torch.Tensor(a)
	model= torch.load('lineups_model5000')

	print('home:',home,'away:',away,model(a))


