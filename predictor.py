import pandas as pd
import numpy as np
import requests
import torch
from selenium import webdriver
from bs4 import BeautifulSoup as bs4

def checker(name):
	if name == 'Goran Dragic':
		name = 'Goran Dragić'
	if name == 'Nikola Jokic':
		name = 'Nikola Jokić'
	return name

x=requests.get('https://www.rotowire.com/basketball/nba-lineups.php')

soup=bs4(x.text,'html.parser')

aways= soup.find_all('ul','lineup__list is-visit')
homes= soup.find_all('ul','lineup__list is-home')

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

data= pd.read_csv('./data/predict.csv')
data.pop('Result')

model2use= input('what model to use? ')
model= torch.load('./models/'+model2use)

file=open('./logs/'+model2use+'_log.txt','a')
for players in games:
	a=np.array([])
	df1=pd.DataFrame()
	for player in players:
		player=checker(player)
		df=data.loc[data['player']==player].tail(1)
		df1=df1.append(df)
	
	away=str(df1.head(1)['team'].values)[2:-2]
	home=str(df1.tail(1)['team'].values)[2:-2]
	
	if len(df1) != 10:
		print(df1)
		print('some player has different name')

	df1=df1[df1.columns[4:]]

	for ar in df1.values:
		ar=np.array(ar)
		a=np.concatenate((a,ar))

	a=torch.Tensor(a)

	file.write(home+','+away+','+date+','+str(float(model(a)))+'\n')
	print('home:',home,'away:',away,model(a))

file.close()
