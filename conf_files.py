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
        alias %s;
    }

    # your Django project's static files - amend as required
    location /static {
        alias %s; 
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }
}
""" 


gunicorn_deamon_conf = """description "Gunicorn daemon for Django project"

start on (local-filesystems and net-device-up IFACE=eth0)
stop on runlevel [!12345]

# If the process quits unexpectedly trigger a respawn
respawn

setuid django
setgid django
chdir /home/django

exec gunicorn \\
    --name={project_root} \\
    --pythonpath={project_root} \\
    --bind=0.0.0.0:9000 \\
    --config /etc/gunicorn.d/gunicorn.py \\
    {project_name}.wsgi:application
 """
 
STAT_MED_INFO = """
MEDIA_URL = '/media/'
MEDIA_ROOT = '{path_to_media}'

STATIC_URL = '/static/'
STATIC_ROOT = '{path_to_static}'
    """

DB_INFO = """
    # added by django one click install script.\n
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': '%s',
           'HOST': 'localhost',
        'PORT': '5432',
       }
   }
    """
 
 
 
