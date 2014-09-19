import json

with open('good-cultures.json','r') as f:

	d = json.loads(f.read())
	
	for key in d.keys():
		if key[0] == '<' or 'DO NOT USE' in key:
			del d[key]
		else:
			print key
		
	with open ('better-cultures.json','w') as f:
		f.write(json.dumps(d,indent=4))	

		

		
	
