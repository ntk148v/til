#!/bin/bash

# Zabbix Server v3.2
# Env: Centos 7.x

# Install requirements packages.
install_requirements()
{
    echo "##### Install and configure Httpd, MariaDB #####"
    yum install httpd php php-mbstring php-pear php-mysql php-gd php-xml php-bcmath mariadb-server -y
    sed -i "s/;date.timezone =/date.timezone = 'Asia/Ho_Chi_Minh'/" /etc/php.ini
    echo "##### Start MariaDB && HTTPD #####"
    systemctl start httpd mariadb
    systemctl enable httpd mariadb
    echo "##### Configure mysql secure #####"
    mysql_secure_installation
    # Check firewall is running or not
    if pgrep firewall ;
    then
        echo "###### Config firewall #####"
        firewall-cmd --add-service=http --permanent
        firewall-cmd --add-service=mysql --permanent
        firewall-cmd --reload
    fi
    echo "##### Done #####"
}

pause_error()
{
    while true
    do
        read -p "Do you want to continue(Y/n) ?: " INPUT_STRING
        case $INPUT_STRING in
            c|C|y|Y|yes|YES"")
                echo ""
                break
            ;;
            n|N|no|NO)

                echo '**********************************************'
                echo "Thanks You Using Script"
                echo '**********************************************'
                exit $1
            ;;
        esac
    done
}

install_zabbix_server()
{
    file_db="/tmp/config.sql"
    echo "##### Install Zabbix #####"
    yum -y install http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm
    yum update
    yum -y install zabbix-get zabbix-server-mysql zabbix-web-mysql
    echo -n "##### Enter Zabbix database password and press [ENTER]:"
    read db_pass
cat > $file_db <<eof
create database zabbix character set utf8 collate utf8_bin;
grant all privileges on zabbix.* to zabbix@'localhost' identified by 'zabbix';
grant all privileges on zabbix.* to zabbix@'%' identified by '$db_pass';
flush privileges;
eof
    while true
    do
        echo "##### Import database as root, enter root's password which is
        configured in prev step #####"
        mysql -u root -e"source $file_db" -p
        if [ $? -eq 0 ]
        then
            echo "##### Configure db success! Username-password: zabbix-$db_pass  #####"
            rm -rf $file_db
            break
        else
            echo "##### Error when configure db #####"
            pause_error
        fi
    done
    echo "##### Import initial schema and data #####"
    zcat /usr/share/doc/zabbix-server-mysql-3.2.*/create.sql.gz | mysql -uzabbix -p zabbix
    echo "##### Start Zabbix server #####"
    systemctl start zabbix-server
    systemctl enable zabbix-server
    setsebool -P httpd_can_connect_zabbix on
    systemctl restart httpd
    echo "##### Done! Now u can access http://<server_ip>/zabbix in a browser.
    Default username/password is Admin/zabbix #####"
}

main()
{
    clear
    install_requirements
    install_zabbix_server
}

main
