import pandas as pd
import numpy as np
import requests
import datetime
#import torch
import joblib
from bs4 import BeautifulSoup as bs4

def checker(name):
	if name == 'Goran Dragic':
		name = 'Goran Dragić'
	if name == 'Nikola Jokic':
		name = 'Nikola Jokić'
	return name

x=requests.get('https://www.rotowire.com/basketball/nba-lineups.php')
print('getting games')
soup=bs4(x.text,'html.parser')

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

# date of games
today=datetime.date.today()
date=today.strftime("%m/%d/%Y")

data= pd.read_csv('./data/predict.csv')
data.pop('Result')

model2use= input('what model to use? ')
#model= torch.load('./models/'+model2use) #### pytorch model
clf= joblib.load('./models/'+model2use) #### scikit model

file=open('./logs/'+model2use+'_log.txt','a')
for players in games:
	a=np.array([])
	df1=pd.DataFrame()
	df2=pd.DataFrame()
	i=0
	for player in players[:5]:
		if i < 5:
			player=checker(player)
			df=data.loc[data['player']==player].tail(1)
			df1=df1.append(df)
			i=i+1
	for player in players[5:]:
		player=checker(player)
		df=data.loc[data['player']==player].tail(1)
		df2=df2.append(df)
	
	away=str(df1.iloc[0]['team'])#[2:-2]
	home=str(df2.iloc[0]['team'])#[2:-2]
	
	if len(df1) != 5:
		print(df1)
		print('some player has different name')
	if len(df2) != 5:
		print(df2)
		print('some player has different name')

	df1=df1.drop(['gameid','date','team','player'],1)
	df2=df2.drop(['gameid','date','team','player'],1)

	summed_df1=pd.DataFrame()
	summed_df2=pd.DataFrame()
	for column in df1.columns:
			summed_df1.at[0,column]=sum(df1[column])
			summed_df2.at[0,column]=sum(df2[column])
	
	df=summed_df1.subtract(summed_df2)
	#df=summed_df1.join(summed_df2,rsuffix='_home')
	
	#a=torch.Tensor(df.values)

	pred=clf.predict(df)
	#pred=model(a)
	file.write(home+','+away+','+date+','+str(float(pred))+'\n')
	print('home:',home,'away:',away,float(pred))

file.close()


