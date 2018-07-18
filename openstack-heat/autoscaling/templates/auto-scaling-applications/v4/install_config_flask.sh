#!/bin/sh

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
. /etc/environment
virtualenv venv
venv/bin/pip install flask gunicorn

# make the cloud user to be the owner of the application
chown -R cloud:cloud app.py
