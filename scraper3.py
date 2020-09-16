from bs4 import BeautifulSoup as bs4
from functions import name2acro2
import requests
import re

with open('trial.txt','w') as file:
	file.write('Player,MP,FG,FGA,FG,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,+/-\n')

	x = requests.get('https://www.basketball-reference.com/leagues/NBA_2020_games-october.html')

	soup=bs4(x.text,'html.parser')
	links=soup.find_all('a',attrs={'href' : re.compile ('/boxscores/[0-9]')})
	for link in links:
		link=link.get('href')
		
		# get game data
		x = requests.get('https://www.basketball-reference.com'+link)
		print(link)

		soup=bs4(x.text,'html.parser')

		# get names
		names=soup.body.find('div',class_="scorebox").find_all('strong')
		names[1]=name2acro2(names[1].text.replace('\n',''))
		names[0]=name2acro2(names[0].text.replace('\n',''))

		date=soup.body.find('div',id='content').h1.text
		date=date[date.find(',')+2:]

		# get scores
		#scores=soup.body.find_all('div',class_="score")

		for team in names:
			if team=='CHA':
				team='CHO' # basketball-reference writes it as CHO idk why
			if team=='BKN':
				team='BRK' # basketball-reference writes it as CHO idk why
			if team=='PHX':
				team='PHO' # basketball-reference writes it as CHO idk why
			# get whole game table
			table=soup.body.find_all('div',attrs={"id":"div_box-"+team+"-game-basic","class":"overthrow table_container"})
			if len(table) > 1:
				print("sómething's wrong mate")
			table=table[0].table

			stats=[]
			lines=table.find_all('tr')
			for line in lines:
				name=line.find('th').text
				stats_line=line.find_all('td')
				if len(stats_line) > 0:
					line=''
					for stat in stats_line:
						line=line+','+stat.text
					if name != 'Team Totals':
						line=team+','+name+line+'\n'
					elif name == 'Team Totals':
						line=team+','+name+line[:-1]+'\n'
					if name != 'Starters' or name != 'Reserves':
						stats.append(line)

			for line in stats:
				file.write(line)


