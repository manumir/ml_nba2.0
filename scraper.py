import time
import os
import sys
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import re

# initiate driver

#driver = webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
driver = webdriver.Firefox(executable_path='../geckodriver')
#driver.get('https://stats.nba.com/gamebooks/?Date=12%2F30%2F2019')# day of games
teams1=['MEM','HOU','BKN','BOS','LAC','NOP','SAC','POR','DET','UTA','CHA','SAS','WAS','TOR','DEN','MIL','ATL','GSW','DAL','ORL','PHI','NYK','LAL','CLE','OKC','MIN','CHI','MIA','PHX','IND']
stripers=[' F,',' G,',' C,']
f=open('data.txt','w')
for i in range(1230):
	driver.get('https://stats.nba.com/game/002180'+str(i+1).zfill(4)+'/')
	time.sleep(6)# seconds
	soup=bs4(driver.page_source,'html.parser')

	# get incative players
	nplaying=soup.find_all('div',class_="game-summary__inactive")
	# formatting incative players
	for x in nplaying:
		x=x.get_text()
		abc=x.split('\n')
	ab=[]
	for x in abc:
		if x != '':
			x=x.strip(' ')
			ab.append(x)
	ab=' '.join(ab)
	lines=list()
	for team in teams1:
		match=re.search(team,ab)
		if match and match.start()>17:
			lines.append(ab[22:match.start()-1])
			lines.append(ab[match.start()+5:])
			break
	
	inactive=[]
	for x in lines:
		x=''.join(x)
		x=x.replace(', ',',')
		x=x.split(',')
		a=[]
		for name in x:
			a.append(name+',,,,,,')
		inactive.append(a)

	# get all that good data
	stuff=soup.find_all('div',class_="nba-stat-table__overflow")
	# get teams names
	teams=[]
	teams_soup=soup.find_all('div',class_="nba-stat-table__caption")
	# get date of game
	date=soup.find_all('div',class_="game-summary__date")
	
	# formatting teams
	for team in teams_soup:
		teams.append(team.get_text(strip=True)+','+date[0].get_text(strip=True))

	# formatting data
	yum=[]
	for x in stuff:
		x=str(x.get_text())[92:]
		x=x.replace("\n"," ")
		yum.append(x)
	yumyum=[]
	for x in yum:
		stop=0
		end=0
		while stop==0:
			match=re.search(r'[A-Z]',x[end:])
			if match:
				x=x[:match.start()+end]+'\n'+x[match.start()+end:]
				end=match.end()+48+end
			else:
				x=x.replace("  "," ")
				yumyum.append(x)
				stop=1
	new=[]
	for x in yumyum:
		new.append(x.split('\n'))
	it=-1
	for x in new:
		for y in x:
			y=' '.join(y.split())
			match=re.search(r'[0-9]',y)
			if match:
				y=y[:match.start()-1]+','+y[match.start():].replace(' ',',')
			
			match=re.search('Totals:,',y)
			if match:
				for player in inactive[it]:
					f.write(teams[it]+','+player+'\n')

			match=re.search('DNP',y)
			if match:
				y=y[:match.start()-1]+',,,,,,'

			match2=re.search('NWT',y)
			if match2:
				y=y[:match2.start()-1]+',,,,,,'
			# strip the F,G,C after the names of the starters
			for stuff in stripers:
				match=re.search(stuff,y)
				if match:
					y=(y[:match.start()]+','+y[match.end():])

			if y!='':
				f.write(teams[it]+','+y+'\n')
			
			if y== '':
				it=it+1

f.close()
driver.quit()






