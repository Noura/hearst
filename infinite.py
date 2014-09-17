from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():

    user_query = request.form['q']

    # we will return our own nicely formatted response
    # of nice artifacts that have images and good descriptions etc
    artifacts = []

    url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
    headers = {}

    # todo: store these as environment vars
    headers['app_key'] = "bd4e742fb930b51e2e6637f415f1742f"
    headers['app_id'] = "26458f3f"

    params = {
        'q': 'objname_txt:' + user_query,
        'wt': 'json',
        }
    r = requests.get(url, params=params, headers=headers)
    d = json.loads(r.text)

    for artifact in d['response']['docs']:
        if 'objdescr_s' not in artifact \
                or 'objname_txt' not in artifact \
                or 'blob_ss' not in artifact:
            continue
        imgurl = img_url(artifact['blob_ss'][0])
        imgr = requests.get(imgurl)
        if imgr.status_code != 200:
            continue
        artifacts.append({
            'name': artifact['objname_txt'],
            'desc': artifact['objdescr_s'],
            'img_url': imgurl,
        })

    print json.dumps(artifacts, indent=4)

    data = json.dumps({'query': user_query,'artifacts': artifacts}, indent=4)
    return data

def img_url(blob_ss):
    return 'https://dev.cspace.berkeley.edu/pahma_project/imageserver/blobs/' + blob_ss + '/derivatives/OriginalJpeg/content'

if __name__ == '__main__':
    app.run(debug=True)





# #2908 Adeline


