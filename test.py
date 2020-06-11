import functions as f

teams1=['Boston Celtics','Brooklyn Nets','New York Knicks','Philadelphia 76ers','Toronto Raptors',
'Chicago Bulls','Cleveland Cavaliers','Detroit Pistons','Indiana Pacers','Milwaukee Bucks',
'Atlanta Hawks','Charlotte Hornets','Miami Heat','Orlando Magic','Washington Wizards',
'Dallas Mavericks','Houston Rockets','Memphis Grizzlies','New Orleans Pelicans','San Antonio Spurs',
'Denver Nuggets','Minnesota Timberwolves','Oklahoma City Thunder','Portland Trail Blazers','Utah Jazz',
'Golden State Warriors','LA Clippers','Los Angeles Lakers','Phoenix Suns','Sacramento Kings']

l=[]
for x in teams1:
	l2=[]
	l2.append(x)
	print(l2,'==',f.name2acro(l2,'nba'))
	l.append(l2)
