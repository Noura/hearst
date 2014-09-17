from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
headers = {
        'app_key': "bd4e742fb930b51e2e6637f415f1742f",
        'app_id': "26458f3f"
}
def img_url(blob_ss):
    return 'https://dev.cspace.berkeley.edu/pahma_project/imageserver/blobs/' + blob_ss + '/derivatives/OriginalJpeg/content'

@app.route('/')
def index():
    return render_template('index.html')

# wrapper for Hearst API query
def api_search(params):
    params['wt'] = 'json'
    r = requests.get(url, params=params, headers=headers)
    return json.loads(r.text)

@app.route('/search', methods=['POST'])
def user_artifacts_search_wrapper():
    key = 'objname_txt'
    val = request.form['q']
    n_results = 10
    return json.dumps(artifacts_search(key, val, n_results))

def artifacts_search(key, val, n_results):
    params = {
            'q': key + ':' + val,
            'start': 0
    }

    artifacts = []
    while len(artifacts) < n_results:
        d = api_search(params)
        #print json.dumps(d, indent=4)
        if len(d['response']['docs']) == 0:
            break

        params['start'] += len(d['response']['docs'])

        for artifact in d['response']['docs']:
            if len(artifacts) >= n_results:
                break
            #print 'verbose thing', json.dumps(artifact, indent=4)
            if 'objdescr_s' not in artifact \
                    or 'objname_txt' not in artifact \
                    or 'blob_ss' not in artifact:
                continue
            imgurl = img_url(artifact['blob_ss'][0])
            imgr = requests.get(imgurl)
            if imgr.status_code != 200:
                continue
            #print 'adding artifact', artifact['objname_txt']
            artifacts.append({
                'name': artifact['objname_txt'],
                'desc': artifact['objdescr_s'],
                'img_url': imgurl,
            })

    data = {'query': val, 'artifacts': artifacts}
    return data

@app.route('/tiles', methods=['POST'])
def tiles_search():
    params = {
            #'q': 'objculturetree_txt:*',
            'facet': 'true',
            'facet.field':'objculturetree_ss',
    }
    d = api_search(params)
    data = json.dumps(d, indent=4)
    #print data

    tiles = []
    for cult in d['facet_counts']['facet_fields']['objculturetree_ss']:
        if cult == 0 or cult == '!Kung' or cult == '@Move to Archaeology':
            continue
        print cult
        artifacts_d = artifacts_search('objculturetree_ss', cult, 1)
        artifacts = artifacts_d['artifacts']
        if len(artifacts) > 0:
            tiles.append(artifacts[0])

    data = json.dumps({'tiles': tiles}, indent=4)
    print data
    return data

if __name__ == '__main__':
    app.run(debug=True)





# #2908 Adeline


