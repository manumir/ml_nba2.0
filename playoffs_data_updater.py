from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4
import re

#driver = webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
teams1=['MEM','HOU','BKN','BOS','LAC','NOP','SAC','POR','DET','UTA','CHA','SAS','WAS','TOR','DEN','MIL','ATL','GSW','DAL','ORL','PHI','NYK','LAL','CLE','OKC','MIN','CHI','MIA','PHX','IND']
stripers=[' F,',' G,',' C,']


name='./data/data19-20_playoffs.txt'

with open(name,'r') as file:
	lines=file.readlines()
	last_id=int(lines[-1][:re.search(',',lines[-1]).start()])
	print(last_id)

driver = webdriver.Chrome(executable_path='../chromedriver')
driver.get('https://stats.nba.com/gamebooks/?Date='+input('month: ')+'%2F'+input('day: ')+'%2F2020')# day of games

WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'nba-stat-table')))

soup=bs4(driver.page_source,'html.parser')

table=soup.find_all('div',class_='nba-stat-table')

links=table[0].find_all('a',attrs={'href' : re.compile ('/game/*')})

new_links=[]
for link in links:
	new_links.append(str(link.get('href')))
print(new_links)

f=open(name,'a')
#f.write('GameId,Team,Date,Date2,Player,MIN,FGM,FGA,FG%,3PM,3PA,3P%,FTM,FTA,FT%,OREB,DREB,REB,AST,TOV,STL,BLK,PF,PTS,+/-\n')
i=last_id+1 
for link in new_links:
	driver.get('https://stats.nba.com'+str(link))
	
	WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'nba-stat-table__overflow')))

	soup=bs4(driver.page_source,'html.parser')

	# get teams names
	teams_soup=soup.find_all('div',class_="nba-stat-table__caption")
	# get date of game
	date=soup.find_all('div',class_="game-summary__date")

	# formatting teams
	teams=[]
	for team in teams_soup:
		team=team.get_text(strip=True)
		teams.append(team)
	date=date[0].get_text(strip=True).replace(',','')

	table=soup.find_all('div',class_="nba-stat-table__overflow")

	lines_away=table[0].tbody.find_all('tr')

	for line in lines_away:
		line=str(line.text)
		line=re.split(r'\s',line)
		line=[x for x in line if x != '']
		line=[x for x in line if x != 'F']
		line=[x for x in line if x != 'G']
		line=[x for x in line if x != 'C']
		line=[x+',' for x in line]
		line.append('\n')
		line=''.join(line)

		# eliminate the comma between the names of the players
		match=re.search(r'\d',line)
		if match:
			name=line[:match.start()-1]
			name=name.replace(',',' ')
			line=name+line[match.end()-2:]
			f.write(str(i)+','+teams[0]+','+date+','+line)

	totals_away=str(table[0].tfoot.tr.text)
	totals_away=re.split(r'\s',totals_away)
	totals_away=[x for x in totals_away if x != '']
	totals_away=[x+',' for x in totals_away]
	totals_away.append('\n')
	totals_away=''.join(totals_away)
	f.write(str(i)+','+teams[0]+','+date+','+totals_away)

	lines_home=table[1].tbody.find_all('tr')

	for line in lines_home:
		line=str(line.text)
		line=re.split(r'\s',line)
		line=[x for x in line if x != '']
		line=[x for x in line if x != 'F']
		line=[x for x in line if x != 'G']
		line=[x for x in line if x != 'C']
		line=[x+',' for x in line]
		line.append('\n')
		line=''.join(line)
		
		# eliminate the comma between the names of the players
		match=re.search(r'\d',line)
		match2=re.search(r'DNP|NWT|DND',line)
		if match and not match2:
			name=line[:match.start()-1]
			name=name.replace(',',' ')
			line=name+line[match.end()-2:]
			f.write(str(i)+','+teams[1]+','+date+','+line)

	totals_home=str(table[1].tfoot.tr.text)
	totals_home=re.split(r'\s',totals_home)
	totals_home=[x for x in totals_home if x != '']
	totals_home=[x+',' for x in totals_home]
	totals_home.append('\n')
	totals_home=''.join(totals_home)
	f.write(str(i)+','+teams[1]+','+date+','+totals_home)

	print(i)
	i=i+1

f.close()
driver.quit()

