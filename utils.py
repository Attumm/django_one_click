import os

def get_db_pass():
    # get the postgres password
    with os.popen('cat /etc/motd.tail | grep Pass') as f:
        password_db = f.read().split()[3]
    return password_db

# get requirements.txt
#with os.popen('locate requirements.txt') as f:
#    path_requirements = f.read()[:-1]




# locating the settings file .py and not .pyc files if present.
def get_path_to_settings():
    sh_settings = 'locate %s/settings.py | grep -w settings.py' % project_name
    with os.popen(sh_settings) as f:
        path_to_settings = f.read()[:-1]
    return path_to_settings

def base_dir_func(path_to_settings):
    #removing settings.py and project_name
     return "/".join(i for i in path_to_settings.split("/")[:-2])

def top_folder_django(path_to_settings):
    #removing settings.py and project_name
     return path_to_settings.split("/")[-3]


path_to_settings = get_path_to_settings()

base_dir = base_dir_func(path_to_settings) + "/"
top_folder = top_folder_django(path_to_settings)

nginx_conf = nginx_conf % (base_dir, base_dir)


