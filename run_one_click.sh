#!/bin/bash

rm -R /home/django/django_project

project_name=$1
path_to_requirements=$(locate requirements.txt)
top_folder=$(python /home/django_one_click/print_top_folder.py $1)

#updatedb
#apt-get update
#apt-get upgrade

# install for postgres
#apt-get install python-psycopg2
#apt-get install libpq-dev

path_to_requirements=$(locate requirements.txt)

#pip install -r $path_to_requirements

python /home/django_one_click/run_script.py $project_name

chown -R django:django 'django/{$top_folder}'
service nginx restart
service gunicorn restart
