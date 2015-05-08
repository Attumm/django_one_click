
#Digital Ocean One click installer

This installer assumes three things <br>
1. There are a media and a static folder in the project <br>
2. There is a requirements.txt file <br>
if not make one with: <br>
pip freeze > requirements.txt <br>
3. This is meant for quickly getting the app online to show others nothing more. <br>

Create an droplet with digital ocean. <br>
Select django image, And then follow the commands. <br>

apt-get install git <br>

cd /home/django <br>
git clone (your-django-project) <br>

cd /home/ <br>
git clone https://github.com/Attumm/django_one_click.git <br>
        
chmod 744 django_one_click/run_one_click.sh <br>

django_one_click/./run_one_click.sh <br>

rm -R django_one_click <br>






