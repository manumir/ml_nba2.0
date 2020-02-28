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
#driver.get('https://stats.nba.com/game/0021801220/')# example game page
f=open('data.txt','w')
gudstuff=[]
for i in range(2):
	it=-1
	driver.get('https://stats.nba.com/game/002180'+str(i+1).zfill(4)+'/')

	time.sleep(7)# seconds
	soup=bs4(driver.page_source,'html.parser')
	stuff=soup.find_all('div',class_="nba-stat-table__overflow")
	teams_soup=soup.find_all('div',class_="nba-stat-table__caption")
	teams=[]
	date=soup.find_all('div',class_="game-summary__date")
	for team in teams_soup:
		teams.append(team.get_text(strip=True)+','+date[0].get_text(strip=True))
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
			match2=re.search('DNP',x)
			if match2:
				print(match2)
				x=x[:match2.end()]+','+x[match2.end()+1:]

			match=re.search(r'[A-Z]',x[end:])
			if match:
				x=x[:match.start()+end-1]+'\n'+x[match.start()+end:]
				end=match.end()+24+end
			else:
				x=x.replace("  "," ")
				yumyum.append(x)
				stop=1

	new=[]
	for x in yumyum:
		new=new+x.split('\n')

	for x in new:
		x=' '.join(x.split())

		match=re.search(r'[0-9]',x)
		if match:
			x=x[:match.start()-1]+','+x[match.start():].replace(' ',',')

		if x == '':
			it=it+1
		else:
			f.write(teams[it]+','+x+'\n')

f.close()
driver.quit()
