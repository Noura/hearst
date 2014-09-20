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
    print '\n\n'+culture_name,
    print '\t'+get_culture_summary(culture_name)  #debug
    culture_data = d[culture_name]
    return jsonify(culture_name=culture_name, culture_summary=get_culture_summary(culture_name), culture_data=culture_data)

def get_culture_summary(culture_name):
    summary = ''
    if culture_name == 'Coptic':
        return wikipedia.summary('Coptic people')
    wiki_results = wikipedia.search( culture_name )
    for result in wiki_results:
        if 'people' in result:
            return first_graf_of(wikipedia.summary(result))
    try:
        return first_graf_of(wikipedia.summary( culture_name ))
    except wikipedia.exceptions.DisambiguationError as e:
        return first_graf_of(wikipedia.summary(e.options[0]))
    except wikipedia.exceptions.PageError as e:
        get_culture_summary(wiki_results[0])

def first_graf_of(paragraphs):
    return paragraphs.split('\n')[0]

if __name__ == '__main__':
    app.run(debug=True)





