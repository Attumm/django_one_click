import sys, os

project_name = sys.argv[1]


# get the postgres password
with os.popen('cat /etc/motd.tail | grep Pass') as f:
 	password_db = f.read().split()[3]

# get requirements.txt
with os.popen('locate requirements.txt') as f:
	path_requirements = f.read()[:-1]




# locating the settings file .py and not .pyc files if present.
sh_settings = 'locate %s/settings.py | grep -w settings.py' % project_name
with os.popen(sh_settings) as f:
	path_to_settings = f.read()[:-1]

def base_dir_func(path_to_settings):
	#removing settings.py and project_name
	 return "/".join(i for i in path_to_settings.split("/")[:-2])

base_dir = base_dir_func(path_to_settings) + "/"
nginx_conf = """upstream app_server {
    server 127.0.0.1:9000 fail_timeout=0;
}

server {
    listen 80 default_server;
    listen [::]:80 default_server ipv6only=on;

    root /usr/share/nginx/html;
    index index.html index.htm;

    client_max_body_size 4G;
    server_name _;

    keepalive_timeout 5;

    # Your Django project's media files - amend as required
    location /media  {
        alias %s/media;
    }

    # your Django project's static files - amend as required
    location /static {
        alias %s/static; 
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }
}""".format(base_dir, base_dir)


gunicorn_deamon = """description "Gunicorn daemon for Django project"

start on (local-filesystems and net-device-up IFACE=eth0)
stop on runlevel [!12345]

# If the process quits unexpectedly trigger a respawn
respawn

setuid django
setgid django
chdir /home/django

exec gunicorn \
    --name={project_name} \
    --pythonpath={project_name} \
    --bind=0.0.0.0:9000 \
    --config /etc/gunicorn.d/gunicorn.py \
    {project_name}.wsgi:application
 """.format(project_name=project_name)

with open('/etc/nginx/sites-enabled/django', 'w') as f:
	f.write(nginx_conf)

with open('/etc/init/gunicorn.conf', 'w') as f:
	f.write(gunicorn_deamon)

with open(path_to_settings, 'w+') as f:
	settings_file_list = f.readlines()
	settings_file = change_settings(settings_file_list)
	f.seek(0)
	f.write(settings_file)

def change_settings(settings_file_list):
	for i in range(len(settings_file)):
		line = settings_file[i]
		if line.startswith('MEDIA_ROOT'):
			settings_file[i] = ""
		elif line.startswith('MEDIA_URL'):
			settings_file[i] = ""
		elif line.startswith('STATIC_ROOT'):
			settings_file[i] = ""
		elif line.startwith('STATIC_URL'):
			settings_file[i] = ""
		elif line.startswith("DATABASES"):
			start_db = i

	# finding the end of DATABASE.
	counter = 0
	for i in range(10, -1, -1):
		if "}" in settings_file[start_db + i]:
			counter += 1
			if counter >= 2:
				break
			end_db = start_db + i

	# removing the old db info
	for i in range(start_db, end_db + 1):
		settings_file[i] = ""


	MEDIA_STATIC_INFO = """
	MEDIA_URL = '/media/'
	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

	STATIC_URL = '/static/'
	STATIC_ROOT = os.path.join(BASE_DIR, 'static')
	"""



	DB_INFO = """
	# added by django one click install script.\n
	DATABASES = {
	       'default': {
	           'ENGINE': 'django.db.backends.postgresql_psycopg2',
	           'NAME': 'django',
	           'USER': 'django',
	           'PASSWORD': '{password_db}',
	           'HOST': 'localhost',
	           'PORT': '5432',
	       }
	   }
	""".format(password_db=password_db)

	settings_file[start_db] = DB_INFO
	settings_file.append(STATIC_MEDIA_INFO)

	return settings_file.join()