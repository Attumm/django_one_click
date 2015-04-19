#!/bin/bash

rm -R /home/django/django_project

updatedb


path_to_requirements=$(locate requirements.txt)

project_name=$(python /home/django_one_click/print_project_name.py)
project_root=$(python /home/django_one_click/print_project_root.py)


#yes | apt-get update
#yes | apt-get upgrade

apt-get update
apt-get upgrade
apt-get install python-psycopg2 libpq-dev
pip install -r $path_to_requirements

# install for postgres
#yes | apt-get install python-psycopg2 libpq-dev

path_to_requirements=$(locate requirements.txt)

#yes | pip install -r $path_to_requirements

python /home/django_one_click/change_conf_files.py $project_name

chown -R django:django django/$project_root

python /home/django/$project_root/manage.py migrate
python /home/django/$project_root/manage.py createsuperuser

service ngnix restart
service gunicorn restart
