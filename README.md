
#Digital Ocean One click installer
apt-get install git

cd /home/django
git clone <your-project>

cd /home/
git clone https://github.com/Attumm/django_one_click.git

chmod 777 django_one_click/run_one_click.sh

django_one_click/./run_one_click.sh

rm -R django_one_click

