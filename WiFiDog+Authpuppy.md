# 1.WiFiDog

# 2. Authpuppy

## 2.1 安装 Apache2
    sudo apt-get install apache2

## 2.2 安装 MySQL
    sudo apt-get install mysql-server mysql-client

## 2.3 安装 PostgreSQL
    sudo apt-get install PostgreSQL

## 2.4 安装 PHPMyAdmin
    sudo apt-get install phpmyadmin

## 2.5 源码安装 php5

### 2.5.1 安装PHP依赖包
    sudo apt-get install openssl curl libmcrypt-dev
    sudo apt-get build-dep php5
    sudo apt-get install libapache2-mod-php5 php5-mysql php5-xsl php5-dev php-apc

### 2.5.2 下载php5.5 
  http://php.net/downloads.php

### 2.5.3 编译安装
  cd ~/Downloads/php-5.5.23
<<<<<<< Updated upstream
  sudo ./configure --enable-opcache --prefix=/opt/php --with-apxs2=/usr/bin/apxs2 --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-pgsql=/usr --with-tidy=/usr --with-curl=/usr/bin --with-openssl-dir=/usr --with-zlib-dir=/usr --with-xpm-dir=/usr --with-pdo-pgsql=/usr --with-pdo-mysql=mysqlnd --with-xsl=/usr --with-ldap --with-xmlrpc --with-iconv-dir=/usr --with-snmp=/usr --enable-exif --enable-calendar --with-bz2=/usr --with-mcrypt=/usr --with-gd --with-jpeg-dir=/usr --with-png-dir=/usr --with-freetype-dir=/usr --enable-mbstring --enable-zip --with-pear --with-libdir=/lib/x86_64-linux-gnu --with-config-file-path=/opt/php
=======
  sudo ./configure --enable-opcache --prefix=/opt/php --with-apxs2=/usr/bin/apxs2 --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-pgsql=/usr --with-tidy=/usr --with-curl=/usr/bin  --with-zlib-dir=/usr --with-xpm-dir=/usr --with-pdo-pgsql=/usr --with-pdo-mysql=mysqlnd --with-xsl=/usr --with-ldap --with-xmlrpc --with-iconv-dir=/usr --with-snmp=/usr --enable-exif --enable-calendar --with-bz2=/usr --with-mcrypt=/usr --with-gd --with-jpeg-dir=/usr --with-png-dir=/usr --with-freetype-dir=/usr --enable-mbstring --enable-zip --with-pear --with-libdir=/lib/x86_64-linux-gnu --with-config-file-path=/opt/php
>>>>>>> Stashed changes
  
  sudo make && sudo make install
## 2.6 Test
    
    sudo vim /etc/apache2/sites-available/000-default.conf

修改/var/www/html 为 /var/www/

在/var/www/目录下创建 phpinfo.php 输入

    <?php
    phpinfo();
    ?>
打开127.0.0.1/phpinfo.php查看返回。

然后到这个网站http://www.authpuppy.org/doc/Getting_Started去下载check_configuration.php,这个文件是检测你的电脑安装authpuppy需要哪些环境，
把check_configuration.php放到/var/www/。

浏览器输入127.0.0.1/check_configuration.php，返回
我配置好的环境

********************************
*                              *
*  symfony requirements check  *
*                              *
********************************

php.ini used by PHP: /etc/php5/apache2/php.ini


** Mandatory requirements **

  OK        PHP version is at least 5.2.4 (5.5.9-1ubuntu4.7)

** Optional checks **

  OK        PDO is installed
  OK        PDO has some drivers installed: mysql
  OK        PHP-XML module is installed
  OK        XSL module is installed
  OK        The token_get_all() function is available
  OK        The mb_strlen() function is available
  OK        The iconv() function is available
  OK        The utf8_decode() is available
  OK        The posix_isatty() is available
  OK        A PHP accelerator is installed
  OK        php.ini has short_open_tag set to off
  OK        php.ini has magic_quotes_gpc set to off
  OK        php.ini has register_globals set to off
  OK        php.ini has session.auto_start set to off
  OK        PHP version is not 5.2.9



192.168.1.1:2060/wifidog/status
