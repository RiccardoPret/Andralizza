from flask import Flask, request, jsonify
import pickle
import os

import urllib.request


app = Flask(__name__)

def apps_perms_listify(s_perms):
	#apps list permissions
	apps_permissions_list = []

	# Split the permissions for every apps
	for single_app_perms in s_perms.split(','):
		tmp = []
		for perm in single_app_perms:
			#permissions of single app
			tmp.append(perm)
		apps_permissions_list.append(tmp)

	return apps_permissions_list

@app.route('/')
def index():
	all_args = request.args.to_dict()
	try:
		perm = all_args['perm']
	except:
		return "Incorrect URL"

	# Listify the request
	perms_list = apps_perms_listify(perm)
	for app_perm in perms_list:
		if len(app_perm) != 20:
			return "Incorrect permission"

	# Get the classifier
	response = urllib.request.urlopen("https://rikyupl.000webhostapp.com/clf.pickle")
	data = response.read()
	clf = pickle.loads(data)

	# Predict the result and send them back
	prediction = clf.predict(perms_list)
	result = ""
	for r in prediction:
		result = result + str(r) + ','
	return str(result[:-1])

if __name__ == '__main__':
	#Probably with gunicorn you don't need this
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)