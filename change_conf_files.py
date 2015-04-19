import sys, os

from conf_files import nginx_conf, gunicorn_deamon_conf
from conf_files import STAT_MED_INFO, DB_INFO


def get_info():
	with os.popen("locate settings.py | grep home/django") as f:
		path = f.read()[-1]
		
	list_items = path.split("/")
    
	with os.popen("locate media | grep home/django") as f:
	    path_to_media = f.readlines()[0][:-1]
    	
	with os.popen("locate static | grep home/django") as f:
		path_to_static = f.readlines()[0][:-1]
		
	with os.popen('cat /etc/motd.tail | grep Pass') as f:
		password_db = f.read().split()[3]
    
	info_dic = {
                "project_name": list_items[-2],
                "project_root": list_items[-3],
                "path_to_settings": path,
                "path_to_static": path_to_static,
                "path_to_media": path_to_media,
                "password_db": password_db,
                }
	return info_dic


def change_nginx_conf(nginx_conf, info_dic):
	nginx_conf = nginx_conf % (info_dic["path_to_media"], info_dic["path_to_static"])
	with open('/etc/nginx/sites-enabled/django', 'w') as f:
		f.write(nginx_conf)
		
		
def change_gunicorn_conf(gunicorn_deamon_conf, info_dic):
	gunicorn_deamon_conf.format(
							project_name=info_dic["project_name"], 
							top_folder=info_dic["project_root"],
							)
	with open('/etc/init/gunicorn.conf', 'w') as f:
		f.write(gunicorn_deamon)


def change_settings_file_list(settings_file_list, info_dic, STAT_MED_INFO, DB_INFO):
	start_db = 0
	lines_to_remove = ('MEDIA_ROOT', 'MEDIA_URL', 'STATIC_ROOT', 'STATIC_URL')
	for i in range(len(settings_file_list)):
		line = settings_file_list[i]
		if line.startswith(lines_to_remove):
			settings_file_list[i] = ""
		elif line.startswith("DATABASES"):
			start_db = i

	if not start_db:
		start_db = len(settings_file_list) - 1
	else:
		# finding the end of DATABASE.
		counter = 0
		for i in range(10, -1, -1):
			if "}" in settings_file_list[start_db + i]:
				counter += 1
				if counter >= 2:
					break
				end_db = start_db + i

		# removing the old db info
		for i in range(start_db, end_db + 1):
			settings_file_list[i] = ""

	DB_INFO % info_dic["password_db"]

	settings_file_list.append(DB_INFO)
	settings_file_list.append(STAT_MED_INFO)
	
	return "".join(settings_file_list)


def change_settings(info_dic, STAT_MED_INFO, DB_INFO):
	with open(path_to_settings, 'r+') as f:
		settings_file_list = f.readlines()
		settings_file = change_settings_file_list(
												settings_file_list, 
												info_dic, 
												STAT_MED_INFO, 
												DB_INFO)
		f.seek(0)
		f.write(settings_file)
		
   
   
if __name__ == "__main__":
	info_dic = get_info
	change_nginx_conf(nginx_conf, info_dic)
	change_gunicorn_conf(gunicorn_deamon_conf, info_dic)
	change_settings(info_dic, STAT_MED_INFO, DB_INFO)
  