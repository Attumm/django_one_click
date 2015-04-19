#!/bin/bash

rm -R /home/django/django_project

updatedb


path_to_requirements=$(locate requirements.txt)

project_name=$(python /home/django_one_click/print_name_project.py)
project_root=$(python /home/django_one_click/print_root_project.py)


yes | apt-get update
yes | apt-get upgrade

# install for postgres
yes | apt-get install python-psycopg2 libpq-dev

path_to_requirements=$(locate requirements.txt)

pip install -r $path_to_requirements

python /home/django_one_click/change_conf_files.py $project_name

chown -R django:django django/$project_root

python /home/django/$project_root/manage.py migrate
python /home/django/$project_root/manage.py createsuperuser

service nginx restart
service gunicorn restart
