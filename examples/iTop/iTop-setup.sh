#!/bin/bash

function start_apache {
	echo "Launching apache2 in foreground with /usr/sbin/apache2ctl -DFOREGROUND -k start"
	/usr/sbin/apache2ctl -DFOREGROUND -k start
}

function stop_apache {
	echo "Stopping  apache2"
	/usr/sbin/apache2ctl stop
}

# Trap to have a clean exit
trap stop_apache HUP INT QUIT KILL TERM


# Main

#Start MySQL and set root password for MySQL
echo "Start MySQL"
/etc/init.d/mysql start
echo "Configure MySQL root password"
mysqladmin -u root password password

#Configure web part
cd /var/www/html
unzip -q -o /tmp/iTop-2.2.0-beta-2371.zip
mkdir -p itop
chmod 777 -R /var/www/html/
cd itop
ln -sf .. web
cd ..
ip a
#sed -i -e 's/Listen 80/Listen 8000/' /etc/apache2/ports.conf
start_apache
