
#Digital Ocean One click installer
apt-get git
cd /home/
git clone https://www.github.com/attumm/one_click_installer.git
git clone yourproject

chmod 777 one_click_installer/run_one_click.sh
one_click_installer/./run_one_click.sh <your_project_name>