#!/bin/sh

export http_proxy="http://10.61.2.237:3128"
export https_proxy="http://10.61.2.237:3128"
cat >/etc/apt/apt.conf <<EOF
Acquire::http::proxy "http://10.61.2.237:3128/";
Acquire::https::proxy "https://10.61.2.237:3128/";
EOF
cat >/etc/environment <<EOF
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
export http_proxy="http://10.61.2.237:3128/"
export https_proxy="https://10.61.2.237:3128/"
export no_proxy="localhost,127.0.0.1"
EOF
. /etc/environment
