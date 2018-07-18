#!/bin/sh

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
