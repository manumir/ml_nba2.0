import time
import os
import sys
start_time = time.time()

from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from selenium.common.exceptions import TimeoutException

currentpath=os.getcwd()
#os.makedirs(str(os.getcwd())+'\\data\\')
path2data=os.path.join(currentpath,"data\\")

# initiate driver
driver = webdriver.Chrome(executable_path='C:/Users/dude/Desktop/chromedriver.exe')
driver.get('https://stats.nba.com/gamebooks/?Date=12%2F30%2F2019')# day of games
driver.get('https://stats.nba.com/game/0021801220/')# example game page

# wait till page loads
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.nba-stat-table__caption")))

# find div of the games
soup=bs4(driver.page_source,'html.parser')
games=soup.find_all('div',class_="nba-stat-table")

games=bs4(str(games[0]),'html.parser')
#print(games.div.table.tbody.text)
links = []

for link in games.find_all('a', attrs={'href': re.compile("^/game")}):
    links.append(link.get('href'))

print(links)
#features = html.table.thead.tr.text #don't need to scrape this multiple times

stuff=soup.find_all('div',class_="nba-stat-table__overflow")
for x in stuff:
	print(x.text)
#stats=html.table.tbody.text
#path=driver.find_element_by_class_name("stats-table-pagination__next")
#path.click()

driver.quit()
#print("scraped in %s seconds" % (time.time() - start_time))
