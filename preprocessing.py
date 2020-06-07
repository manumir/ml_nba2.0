import pandas as pd
"""
with open('data2.csv','r') as f :
	lines=f.readlines()
	w=open('data3.csv','w')
	for line in lines:
		search=line.find('Totals:,')
		if search > -1:
			print(line)
			line=line[:search]+'Totals:,99:99,'+line[search+len('Totals:,'):]
			print(line)
		w.write(line)
	w.close()
"""
f=pd.read_csv('data.txt')

date=list(f['Date'].values)
date2=list(f['Date2'].values)

new=[]
for x in range(len(date)):
	new.append(str(date[x])+' '+str(date2[x]))

f=f.drop(['Date2'],1)
f['Date']=new

nan_rows = f[f.isnull().T.any().T]
print(nan_rows)

print(f.head(30))
