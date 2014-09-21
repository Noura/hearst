import requests, json

# list of all parent cultures
parents = [
	"@Africa",
	"@Alaskan tribes",
	"@Algeria",
	"@Amazonian cultures",
	"@Andaman Islands",
	"@Angola",
	"@Arctic tribes",
	"@Argentina",
	"@Asia",
	"@Australia",
	"@Benelux",
	"@Bolivia",
	"@Botswana",
	"@Brazil",
	"@British Columbia tribes",
	"@British Isles",
	"@Burkina Faso",
	"@Burundi",
	"@California Desert tribes",
	"@California tribes",
	"@Cambodia",
	"@Cameroon",
	"@Canadian tribes",
	"@Caribbean",
	"@Central Africa",
	"@Central African Republic",
	"@Central America",
	"@Central California Tribes",
	"@Central Northwest Coast Tribes",
	"@Central Puget Sound tribes",
	"@Chile",
	"@China",
	"@Colombia",
	"@Columbia River tribes",
	"@Congo",
	"@Czechoslovakia",
	"@Democratic Republic of the Congo",
	"@Denmark",
	"@East Asia",
	"@Eastern Africa",
	"@Eastern Europe",
	"@Eastern Oregon tribes",
	"@Eastern Washington tribes",
	"@Ecuador",
	"@Egypt",
	"@England",
	"@Ethiopia",
	"@Europe",
	"@Fiji",
	"@France",
	"@Gabon",
	"@Germany",
	"@Ghana",
	"@Great Basin tribes",
	"@Great Lakes tribes",
	"@Guinea",
	"@Guinea-Bissau",
	"@Guyana",
	"@Hawaii",
	"@Horn of Africa",
	"@Hungary",
	"@India",
	"@Indonesia",
	"@Ira needs to determine",
	"@Ireland",
	"@Irian Jaya",
	"@Italian peninsula",
	"@Italy",
	"@Ivory Coast",
	"@Japan",
	"@Kenya",
	"@Kiriwina Islands",
	"@Laos",
	"@Liberia",
	"@Lower Columbia River Tribes",
	"@Madagascar",
	"@Mainland Southeast Asia",
	"@Malawi",
	"@Malaysia",
	"@Maldives",
	"@Mali",
	"@Maritime Southeast Asia",
	"@Massim cultural area",
	"@Melanesia",
	"@Mexican tribes",
	"@Micronesia",
	"@Mongolia",
	"@Morocco",
	"@Move to Archaeology",
	"@Mozambique",
	"@Myanmar",
	"@Namibia",
	"@Netherlands",
	"@New Guinea (Papua Island)",
	"@Nigeria",
	"@North America",
	"@North America historic" ]


url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
headers = {}

headers['app_key'] = "bd4e742fb930b51e2e6637f415f1742f"
headers['app_id'] = "26458f3f"


# helpers
def img_url(blob_ss):
    return 'https://dev.cspace.berkeley.edu/pahma_project/imageserver/blobs/' + blob_ss + '/derivatives/OriginalJpeg/content'

def api_search(params):
    params['wt'] = 'json'
    r = requests.get(url, params=params, headers=headers)
    return json.loads(r.text)


# code
def artifacts_search(key, val, n_results):

    print '\n\t' + val,

    params = {
            'q': key + ':' + val,
            'start': 0
    }

    artifacts = {}
    while len(artifacts.keys()) < n_results:
        d = api_search(params)
        #print json.dumps(d, indent=4)
        if len(d['response']['docs']) == 0:
            break

        params['start'] += len(d['response']['docs'])

        for artifact in d['response']['docs']:
            if len(artifacts.keys()) >= n_results:
                break
            #print 'verbose thing', json.dumps(artifact, indent=4)
            if 'objdescr_s' not in artifact \
                    or 'blob_ss' not in artifact \
                    or 'objmusno_s' not in artifact:
                continue
            imgurl = img_url(artifact['blob_ss'][0])
            imgr = requests.get(imgurl)
            if imgr.status_code != 200:
                continue
            print '.',
            #print 'adding artifact', artifact['objname_txt']
            artifacts[artifact['objmusno_s']] = imgurl

    return artifacts


# iterate through all parent cultures
for parent_culture in parents:

	cultures = {}

	print parent_culture

	# find all child cultures of parent
	params = {
	    'q': 'objculturetree_ss:' + parent_culture,
	    'wt': 'json',
	    'facet':'true',
	    'facet.field':'objculturetree_ss'
	    }

	r = requests.get(url, params=params, headers=headers)
	d = json.loads(r.text)

	# for up to 6 top (most artifacts) child cultures, find up to 35 artifacts with images associated
	subcults = {}
	counter = 0
	for c in d['facet_counts']['facet_fields']['objculturetree_ss']:
		if type(c) == int or c[0] == '@':
			continue
		counter += 1
		if counter > 6:
			break	
		imaged_results = artifacts_search('objculturetree_ss',c,35)
		subcults[c] = imaged_results

	cultures.update( subcults )

	# filter out those artifacts with odd names
        for key in cultures.keys():
		if key[0] == '<' or 'DO NOT USE' in key:
			del cultures[key]

	# write to a json file
	with open('culturelist.json','a') as f:
		f.write(json.dumps(cultures,indent=4))
