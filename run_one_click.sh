#!/bin/bash

rm -R /home/django/django_project

updatedb

project_name=$1
path_to_requirements=$(locate requirements.txt)
top_folder=$(python /home/django_one_click/print_top_folder.py $1)


yes | apt-get update
yes | apt-get upgrade

# install for postgres
yes | apt-get install python-psycopg2
yes | apt-get install libpq-dev

path_to_requirements=$(locate requirements.txt)

yes | pip install -r $path_to_requirements

python /home/django_one_click/run_script.py $project_name

chown -R django:django django/$top_folder

python /home/django/$top_folder/manage.py migrate
python /home/django/$top_folder/manage.py createsuperuser

service ngnix restart
service gunicorn restart
