#!/bin/sh

# configure supervisor to run a private gunicorn web server, and
# to autostart it on boot and when it crashes
# stdout and stderr logs from the server will go to /var/log/cloud
mkdir /var/log/cloud
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
