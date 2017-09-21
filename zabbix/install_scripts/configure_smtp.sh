#!/bin/bash

# Centos 7

use_smtp_instead_of_postfix()
{
    # By default Centos use postfix to relay email.
    systemctl stop postfix
    systemctl disable postfix
    echo '###### Choose ssmtp! ######'
    alternatives --config mta
}

install_and_config_ssmtp()
{
    yum install ssmtp mailx -y
    use_smtp_instead_of_postfix
    echo '##### Config ssmtp, follow sample configs bellow #####'
cat << EOF
root=gmail-username@gmail.com
mailhub=smtp.gmail.com:587
rewriteDomain=your_local_domain # Result of domainname command, if none - localhost.
hostname=your_local_FQDN # Result of hostname -f command.
UseTLS=Yes
UseSTARTTLS=Yes
AuthUser=Gmail_username
AuthPass=Gmail_password
FromLineOverride=YES
EOF
    sleep 10
    vim /etc/ssmtp/ssmtp.conf
}

get_alertscript()
{
    cd /usr/lib/zabbix/alertscripts/
    wget https://gist.githubusercontent.com/superdaigo/3754055/raw/e28b4b65110b790e4c3e4891ea36b39cd8fcf8e0/zabbix-alert-smtp.sh
    mv zabbix-alert-smtp.sh zabbix-alert-smtp.py
    chmod 755 zabbix-alert-smtp.py
    echo '##### Change Gmail Account and Password #####'
    sleep 5
    vim zabbix-alert-smtp.py
}

main()
{
    echo '##### Install and config SSMTP #####'
    install_and_config_ssmtp
    echo '##### Get AlertScript #####'
    get_alertscript
    echo '##### Done #####'
}

main
