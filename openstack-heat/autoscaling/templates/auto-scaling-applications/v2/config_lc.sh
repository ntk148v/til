#!/bin/sh
cat >>/home/cloud/.bashrc <<EOF
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
EOF

. /home/cloud/.bashrc
