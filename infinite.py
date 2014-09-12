import requests
import json

url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
headers = {}
headers['app_key'] = "bd4e742fb930b51e2e6637f415f1742f"
headers['app_id'] = "26458f3f"

params = {
    #'q': 'objculturetree_txt:Arctic',
    'q': 'objmaterials_txt:gold',
    'wt': 'json',
    'indent': True,
    #'facet': 'true',
    #'facet.field':'objculturetree_ss'
    }
r = requests.get(url, params=params, headers=headers)

print r.url
print r.status_code
print json.dumps(json.loads(r.text), indent=4)


#2908 Adeline


