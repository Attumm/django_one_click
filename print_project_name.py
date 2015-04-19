from os import popen


def get_project_name():
    with popen("locate settings.py | grep home/django") as f:
        path = f.read()[-1]
    return path.split("/")[-2]


print get_project_name()