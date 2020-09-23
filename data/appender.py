import glob

files=glob.glob('data*.txt')

all_lines=[]
for file in files:
	print(file)
	with open(file,'r') as f:
		lines=f.readlines()
		all_lines=all_lines+lines[1:]

with open('all_data.txt','w') as f:
	f.write(lines[0])
	for line in all_lines:
		f.write(line)
