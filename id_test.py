import requests, json


url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
headers = {}

headers['app_key'] = "bd4e742fb930b51e2e6637f415f1742f"
headers['app_id'] = "26458f3f"



params = {
    'q': 'objmusno_s:5-16488',
    'wt': 'json',
    }

r = requests.get(url, params=params, headers=headers)
d = json.loads(r.text)

print d
