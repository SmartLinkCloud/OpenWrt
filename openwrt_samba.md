由于OpenWRT添加用户需要额外安装shadow软件包，而OpenWRT本身又不太建议这样做，所以本文直接以root用户共享为例说明一下配置过程。
#1. 安装Samba服务

执行如下命令安装Samba服务：

opkg update
opkg install samba36-server

注：上面的samba36-server是本文发布时的Samba服务软件包名称，其中数字36表示3.6.X版本，以后Samba版本更新的话可能找不到这个软件包，这个时候执行opkg list | grep samba搜一下就好。
#2. 配置全局共享参数

配置文件路径为/etc/samba/smb.conf，将[global]中的invalid users = root注掉，像下面的样子：

[global]
netbios name = |NAME|
display charset = |CHARSET|
interfaces = |INTERFACES|
server string = |DESCRIPTION|
unix charset = |CHARSET|
workgroup = |WORKGROUP|
browseable = yes
deadtime = 30
domain master = yes
encrypt passwords = true
enable core files = no
guest account = nobody
guest ok = yes
# invalid users = root
local master = yes
load printers = no
map to guest = Bad User
max protocol = SMB2
min receivefile size = 16384
null passwords = yes
obey pam restrictions = yes
os level = 20
passdb backend = smbpasswd
preferred master = yes
printable = no
security = user
smb encrypt = disabled
smb passwd file = /etc/samba/smbpasswd
socket options = TCP_NODELAY IPTOS_LOWDELAY
syslog = 2
use sendfile = yes
writeable = yes

#3. 配置共享目录

例如要添加一个名称为home的共享，共享路径为/home，允许root用户读写操作，在/etc/samba/smb.conf配置文件中增加如下信息：

[home]
path = /home
valid users = root
read only = no
guest ok = yes
create mask = 0750
directory mask = 0750

#4. 配置共享密码

Samba的共享用户密码是单独配置的，执行下面的命令将root添加为共享用户，同时按照命令提示设置共享密码。

smbpasswd -a root

#5. 完成

配置完成后，启动Samba服务即可。

/etc/init.d/samba start

#6.smbclient
smbclient //服务器地址/目录 -U 用户名％密码

