#!/bin/bash
trap ctrl_c INT

function ctrl_c() {
    echo "# Ctrl + C happened, clean up"
    echo "# Remove containers"
    docker rm -f netshoot nginx httpie
    echo "# Remove networks"
    docker network rm bridge1 bridge2
}

function usage() {
    cat << EOM
    Usage:
    $(basename $0) <your external ip address>

EOM
    exit 0
}

[ -z $1 ] && { usage ;}


echo "# Create bridge networks"
docker network create --subnet 192.168.1.0/24 bridge1

echo "# Start nginx server with network bridge1"
docker run -d --name nginx --net bridge1 -p 8000:80 nginx:alpine

echo "# Start netshoot with nginx network namespace"
docker run -d --name netshoot --net container:nginx nicolaka/netshoot tcpdump -nni any tcp

docker logs -f --tail 100 netshoot
