from os import popen

def get_project_root():
    with popen("locate settings.py | grep home/django") as f:
        path = f.read()[:-1]
    return path.split("/")[-3]

print get_project_root()
