from os import path, makedirs
import urllib.request
import sys
from ext import dvm
import utils

# SETTINGS
UTIL_FILES_PATH = "./app_files/"
PERMS_PATH = UTIL_FILES_PATH + "/parsed_permissions/"
LOGS_PATH = "./logs/"
URL_WEBAPP = "https://andralizza.herokuapp.com/"


def setup_environment():
	if not path.exists(PERMS_PATH):
		makedirs(PERMS_PATH)
	if not path.exists(LOGS_PATH):
		makedirs(LOGS_PATH)


def extract_permissions():
	apks_path = ""
	try:
		apks_path = sys.argv[1]
		if apks_path[-1] != '/':
			apks_path = apks_path + '/'
	except IndexError as e:
		print("The program needs the apks folder as parameter")
		exit(-1)

	file_list = utils.scan_dir_files(apks_path)

	for file in file_list:
		try:
			apk = dvm.APK(apks_path + file)

			with open(PERMS_PATH + str(file) + ".txt", 'w') as fp:
				for perm in apk.get_permissions():
					fp.write(perm + "\n")

		except Exception as e:
			utils.write_log("main_apks_problems.txt", "File: " + str(file) + "\tException: " + str(e))


def get_top_perms():
	top_perms = []
	with open(UTIL_FILES_PATH + "top_perms.txt", 'r') as fp:
		for perm in fp:
			top_perms.append(perm.split("\n")[0])
	return top_perms


def get_features_list(apps_perms_file_list):
	# Dictionary: key=perms_filename, value=parsed_perms
	apps_features_dict = {}
	top_perms = get_top_perms()

	for app_perms_file in apps_perms_file_list:
		pl = []
		with open(PERMS_PATH + app_perms_file, 'r') as man:
			p_l = []
			# Get the permissions list from the file
			for perm in man:
				# WARNING: Take only the last part, without the '\n'. The permissions produced have an empty line so it works
				# also for the last line but still it should be better another solution more general
				p = perm.split('.')[-1][:-1]
				p_l.append(p)
			# Check which permissions are in the top 20
			for top_perm in top_perms:
				if top_perm in p_l:
					pl.append(1)
				else:
					pl.append(0)
		apps_features_dict[app_perms_file] = pl
	return apps_features_dict


def write_parsed_permissions(apps_feats_list):
	with open(UTIL_FILES_PATH + "perms.txt", 'w') as f:
		items = sorted(apps_feats_list.values())
		for value in items:
			for digit in value:
				f.write(str(digit))
			f.write('\n')


def parse_permissions():
	# Get all the permissions files
	apps_perms_file_list = utils.scan_dir_files(PERMS_PATH)
	# Add the permissions in a list following the classifier syntax
	apps_features_dict = get_features_list(apps_perms_file_list)
	# Write the parse permissions/features
	write_parsed_permissions(apps_features_dict)


def build_get_request():
	url = ""
	with open(UTIL_FILES_PATH + "perms.txt", 'r') as a:
		lines = a.readlines()
		for row in lines:
			url = url + row.split("\n")[0] + ','

	return URL_WEBAPP + "?perm=" + url[:-1]


def get_result():
	s = ""
	url = build_get_request()
	binary = urllib.request.urlopen(url)
	content = binary.read().decode(binary.headers.get_content_charset())

	with open(UTIL_FILES_PATH + "perms.txt", 'r') as perm_file:
		for res in content.split(','):
			s = s + perm_file.readline()[:-1] + ":\t" + ("Malware" if res == '1' else "Safe") + '\n'
	print(s)


def debug_mode(is_debug):
	if is_debug:
		global URL_WEBAPP
		URL_WEBAPP = "http://127.0.0.1:5000/"


if __name__ == '__main__':
	utils.reset_environment()
	debug_mode(False)
	setup_environment()
	extract_permissions()
	parse_permissions()
	get_result()
