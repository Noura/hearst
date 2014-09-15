from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():

	user_query = request.form['q']

	url = 'https://apis-qa.berkeley.edu/hearst_museum/select'
	headers = {}

	# todo: store these as environment vars
	headers['app_key'] = "bd4e742fb930b51e2e6637f415f1742f"
	headers['app_id'] = "26458f3f"

	params = {
	    #'q': 'objculturetee_txt:Arctic',
	    #'q': 'objmaterials_txt:gold',
	    'q': 'objname_txt:' + user_query,
	    'wt': 'json',
	    'indent': True,
	    #'facet': 'true',
	    #'facet.field':'objculturetree_ss'
	    }
	r = requests.get(url, params=params, headers=headers)

	return json.dumps(json.loads(r.text), indent=4)

if __name__ == '__main__':
    app.run(debug=True)





# #2908 Adeline


