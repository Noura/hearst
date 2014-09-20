from flask import Flask, render_template, request, jsonify
import requests, json, random, wikipedia

app = Flask(__name__)

url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
headers = {
        'app_key': "bd4e742fb930b51e2e6637f415f1742f",
        'app_id': "26458f3f"
}

filename = 'even-better-cultures.json'
d = {}
with open(filename, 'r') as f:
    d = json.loads(f.read())

@app.route('/')
def index():
    return render_template('index.html')

# wrapper for Hearst API query
def api_search(params):
    params['wt'] = 'json'
    r = requests.get(url, params=params, headers=headers)
    return json.loads(r.text)

@app.route('/getculture', methods=['GET'])
def get_culture():
    c_i = random.randint(0,len(d.keys())-1)
    culture_name = d.keys()[c_i]
    print get_cultural_summary(culture_name).split('\n')[0]
    culture_data = d[culture_name]
    return jsonify(culture_name=culture_name, culture_data=culture_data)

def get_cultural_summary(culture_name):
    wiki_results = wikipedia.search( culture_name )
    for result in wiki_results:
        if 'people' in result:
            return wikipedia.summary(result)
    try:
        return wikipedia.summary( culture_name )
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0])

if __name__ == '__main__':
    app.run(debug=True)





