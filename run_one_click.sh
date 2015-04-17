!/bin/bash


project_name=$1
path_to_requirements=$(locate requirements.txt)
top_folder=$(python /home/django_one_click/print_top_folder.py $1)

updatedb
apt-get update
apt-get upgrade

# install for postgres
apt-get install python-psycopg2
apt-get install libpq-d

path_to_requirements=$(locate requirements.txt)

pip install -r $path_to_requirements

#chmod 777 /home/run_script.py
python /home/run_script.py project_name


chown -R django:django $top_folder
service nginx restart
service gunicorn restart