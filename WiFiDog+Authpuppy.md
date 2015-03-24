# Authpuppy
## Installing xampp
### Downloading xampp 5.5
APC has some bugs with 5.6 running,so select 5.5.
    https://www.apachefriends.org/download.html

    cd ~/Downloads
    sudo chmod +x xampp-linux-x64-5.5.19-0-installer.run 
    ./xampp-linux-x64-5.5.19-0-installer.run 
    sudo ./xampp-linux-x64-5.5.19-0-installer.run

然后到这个网站http://www.authpuppy.org/doc/Getting_Started去下载check_configuration.php这个文件是检测你的电脑安装authpuppy需要哪些环境，下面是我配置好的环境

	********************************
	*                              *
	*  symfony requirements check  *
	*                              *
	********************************

	php.ini used by PHP: /opt/lampp/etc/php.ini


	** Mandatory requirements **

	  OK        PHP version is at least 5.2.4 (5.5.19)

	** Optional checks **

	  OK        PDO is installed
	  OK        PDO has some drivers installed: mysql, pgsql, sqlite
	  OK        PHP-XML module is installed
	  OK        XSL module is installed
	  OK        The token_get_all() function is available
	  OK        The mb_strlen() function is available
	  OK        The iconv() function is available
	  OK        The utf8_decode() is available
	  OK        The posix_isatty() is available
	[[WARNING]] A PHP accelerator is installed: FAILED
		    *** Install a PHP accelerator like APC (highly recommended) ***
	[[WARNING]] php.ini has short_open_tag set to off: FAILED
		    *** Set it to off in php.ini ***
	  OK        php.ini has magic_quotes_gpc set to off
	  OK        php.ini has register_globals set to off
	  OK        php.ini has session.auto_start set to off
	  OK        PHP version is not 5.2.9


