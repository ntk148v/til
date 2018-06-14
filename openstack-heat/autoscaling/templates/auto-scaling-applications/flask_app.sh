#!/bin/bash -v
cat >>/home/cloud/.bashrc <<EOF
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
EOF
source /home/cloud/.bashrc
export http_proxy="http://10.61.2.237:3128"
export https_proxy="http://10.61.2.237:3128"
cat >/etc/apt/apt.conf <<EOF
Acquire::http::proxy "http://10.61.2.237:3128/";
Acquire::https::proxy "https://10.61.2.237:3128/";
EOF
cat >/etc/environment <<EOF
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
http_proxy="http://10.61.2.237:3128/"
https_proxy="https://10.61.2.237:3128/"
EOF
source /etc/environment

apt update
apt install build-essential python python-dev python-virtualenv nginx supervisor git -y
# Create a user to run the server process - skip this step if your image already has one.
# adduser --disabled-password --gecos "" cloud
# Install a tiny application
cd /home/cloud
cat >app.py <<EOF
#!/usr/bin/env python
import socket
from flask import Flask

hostname = socket.gethostname()
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from {0}!" . format(hostname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
EOF

# create virtualenv and install dependencies
virtualenv venv
venv/bin/pip install flask gunicorn

# make the cloud user to be the owner of the application
chown -R cloud:cloud app.py

# configure supervisor to run a private gunicorn web server, and
# to autostart it on boot and when it crashes
# stdout and stderr logs from the server will go to /var/log/cloud
# mkdir /var/log/cloud
cat >/etc/supervisor/conf.d/cloud.conf <<EOF
[program:cloud]
command=/home/cloud/venv/bin/gunicorn -b 127.0.0.1:8000 -w 4 --chdir /home/cloud --log-file - app:app
user=cloud
autostart=true
autorestart=true
stderr_logfile=/var/log/cloud/stderr.log
stdout_logfile=/var/log/cloud/stdout.log
EOF
supervisorctl reread
supervisorctl update
systemctl restart supervisor
systemctl enable supervisor

# configure nginx as the front-end web server with a reverse proxy
# rule to the gunicorn server
cat >/etc/nginx/sites-available/cloud <<EOF
server {
    listen 80;
    server_name _;
    access_log /var/log/nginx/cloud.access.log;
    error_log /var/log/nginx/cloud.error.log;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_redirect off;
        proxy_set_header HOST \$host;
        proxy_set_header X-REAL-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF
rm -f /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/cloud /etc/nginx/sites-enabled/
systemctl restart nginx
