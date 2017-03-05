from shutil import rmtree
from os import remove, listdir
from os.path import isfile, join

APP_FILES = "./app_files/"
LOGS_PATH = "./logs/"


def scan_dir_files(path, alpha_sorted=False):
	try:
		files = [f for f in listdir(path) if isfile(join(path, f))]
	except Exception as e:
		write_log("utils_scan_problem.txt", str(e))
		exit(-1)

	return sorted(files) if alpha_sorted else files


def write_log(file_path, s, default_path=True):
	path = LOGS_PATH+file_path if default_path else file_path

	with open(path, 'a') as fp:
		fp.write(s+'\n')


def reset_environment():
	file_list = ["perms.txt"]
	folder_list = ["parsed_permissions/"]

	for f in file_list:
		try:
			remove(APP_FILES+f)
		except:
			write_log("utils_reset_problems.txt", "Impossible to remove "+str(f))

	for f in folder_list:
		rmtree(APP_FILES+f, ignore_errors=True)

reset_environment()
