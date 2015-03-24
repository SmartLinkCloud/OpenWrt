# Authpuppy


## 2.1 Installing Apache2
	sudo apt-get install apache2

## 2.2 Installing PHP useing src

### 2.2.1 Building the dependencies for PHP
sudo apt-get build-dep php5

### 2.2.2 Downloading php5.5 
http://php.net/downloads.php

### 2.2.3 make && sudo make install
cd ~/Downloads/php-5.5.23
./configure --enable-opcache --prefix=/opt/php
make && sudo make install

## 2.3 Installing MySQL
	sudo apt-get install mysql-server mysql-client

## 2.4 Installing PHPMyAdmin
	sudo apt-get install phpmyadmin

## 2.5 Test

然后到这个网站http://www.authpuppy.org/doc/Getting_Started去下载check_configuration.php,这个文件是检测你的电脑安装authpuppy需要哪些环境，

sudo vim /etc/apache2/sites-available/000-default.conf
change /var/www/html to /var/www/

put check_configuration.php to /var/www/

and type 127.0.0.1/check_configuration.php in firefox web browser.

下面是我配置好的环境

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
[[WARNING]] XSL module is installed: FAILED
            *** Install and enable the XSL module (recommended for Propel) ***
  OK        The token_get_all() function is available
  OK        The mb_strlen() function is available
  OK        The iconv() function is available
  OK        The utf8_decode() is available
  OK        The posix_isatty() is available
[[WARNING]] A PHP accelerator is installed: FAILED
            *** Install a PHP accelerator like APC (highly recommended) ***
  OK        php.ini has short_open_tag set to off
  OK        php.ini has magic_quotes_gpc set to off
  OK        php.ini has register_globals set to off
  OK        php.ini has session.auto_start set to off
  OK        PHP version is not 5.2.9

#### Install APC
APC在PHP5.4及以下版本是性能最好的代码缓存。

不过PHP升级到5.5及以上后，APC不再有效。需要使用Zend的OpCache扩展。

要启用Opcache扩展，有两步：

#### Set short_open_tag

sudo vim /opt/lampp/etc/php.ini
Set short_open_tag to off in php.ini

