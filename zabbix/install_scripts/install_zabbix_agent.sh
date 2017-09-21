#!/bin/bash

# Zabbix Agent v3.2
# Env:Centos 7.2

install_zabbix_agent()
{
    echo "##### Install Zabbix repository #####"
    yum -y install http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm
    yum update
    echo "##### Install Zabbix Agent #####"
    yum install zabbix-agent -y
    echo -n "##### Enter Zabbix Server IP Address and press [ENTER]: "
    read zabbix_server_ip
    echo "##### Config Zabbix Agent #####"
    sed -i "/# Server=/d" /etc/zabbix/zabbix_agentd.conf
    sed -i "/# ServerActive=/d" /etc/zabbix/zabbix_agentd.conf
    sed -i "/# Hostname=/d" /etc/zabbix/zabbix_agentd.conf
    sed -i "s/.*Server=.*/Server=$zabbix_server_ip/" /etc/zabbix/zabbix_agentd.conf
    sed -i "s/.*ServerActive=.*/ServerActive=$zabbix_server_ip/" /etc/zabbix/zabbix_agentd.conf
    sed -i "s/.*Hostname=.*/Hostname=$HOSTNAME/" /etc/zabbix/zabbix_agentd.conf
    echo "##### Start Zabbix Agent #####"
    systemctl start zabbix-agent
    systemctl enable zabbix-agent
    echo "##### Done #####"
}

install_zabbix_agent
