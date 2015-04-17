import sys, os
project_name = sys.argv[1]

sh_settings = 'locate %s/settings.py | grep -w settings.py' % project_name
with os.popen(sh_settings) as f:
	path_to_settings = f.read()[:-1]


def top_folder_django(path_to_settings):
	#removing settings.py and project_name
	 return path_to_settings.split("/")[-2]

print top_folder_django(path_to_settings)