#!/bin/bash
echo "# Start containers"
docker rm -f ctn1 ctn2
docker run --name ctn1 -d alpine:3.17 sleep 30d
docker run --name ctn2 -d alpine:3.17 \
  sh -c 'while true; do echo -e "HTTP/1.0 200 OK\r\n\r\nWelcome" | nc -l -p 80; done'

# echo "# Check ip addresses of the containers"
# nsenter-ctn ctn1 -n ip a
# nsenter-ctn ctn2 -n ip a

# echo "# Connectivity test"
# nsenter-ctn ctn1 -n arping 172.17.0.3
# nsenter-ctn ctn2 -n tcpdump -i eth0 arp

# nsenter-ctn ctn1 -n ping 172.17.0.3 -c 2

# nsenter-ctn ctn1 -n curl 172.17.0.3:80
# nsenter-ctn ctn2 -n tcpdump -nn -i eth0

# echo "# Drop ARP packets"
# Compile to BPF code
# clang -O2 -Wall -target bpf -c drop-arp.c -o drop-arp.o
# Add a tc classifier
# nsenter-ctn ctn2 -n tc qdisc add dev eth0 clsact
# Load and attach program (read program from drop-arp.o's "ingress" section) to eth0's ingress hook
# nsenter-ctn ctn2 -n tc filter add dev eth0 ingress bpf da obj drop-arp.o sec ingress
# Check the filter we've added just now
# nsenter-ctn ctn2 -n tc filter show dev eth0 ingress

# Cleanup
# nsenter-ctn ctn2 -n tc qdisc del dev eth0 clsact 2>&1 >/dev/null
# nsenter-ctn ctn2 -n tc filter show dev eth0 ingress
