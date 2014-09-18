import requests


url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
headers = {
        'app_key': "bd4e742fb930b51e2e6637f415f1742f",
        'app_id': "26458f3f"
}
def img_url(blob_ss):
    return 'https://dev.cspace.berkeley.edu/pahma_project/imageserver/blobs/' + blob_ss + '/derivatives/OriginalJpeg/content'


def depth_traversal(nodes):
    for node in nodes:
        if node == None:
            continue


def get_subcultures(culture):


def visit(culture):
    params = {
            'q': 'objculturetree_txt:' + culture
    r = requests.get(url, params=params, headers=headers)
    artifacts = artifact_search(culture)
    return culture + ': ' + len(artifacts)

def api_search(params):
    params['wt'] = 'json'
    r = requests.get(url, params=params, headers=headers)
    return json.loads(r.text)

def artifacts_search(culture):
    params = {
            'q': 'objculturetree_txt:' + culture,
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

    return artifacts

