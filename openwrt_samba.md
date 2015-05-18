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



一.为什么要用Samba？
    Samba的主要任务就是实现Linux系统和Windows系统之间的资源共享。我们现在是要在Linux下配置Samba，让Windows的用户可以访问你 配置好之后的PC。

二.需要的软件？
    我是在ubuntu上实现的，所以我只需在配置好ubuntu的更新源之后，在终端中使用一下两句命令，就可以安装Samba的软件包
    $sudo apt-get install smaba
    $sudo apt-get install smbfs

三.Samba服务的组成
    Samba的核心是两个守护进程smbd和nmbd。当然，它们的配置信息都保存在/etc/samba/smb.conf里面。
    其中smbd处理Samba软件与Linux协商，nmbd使其他主机能浏览Linux服务器。

四.Samba的配置文件的语法
    配置文件就放在/etc/samba/下，名字叫作smb.conf。如果怕改了之后有问题，可以备份一份。
    执行如下命令进行备份（事实上就是复制一份，并且改名）
    $sudo cp /etc/samba/smb.conf /etc/samba/smb_conf_backup
    一个完整的smb.conf配置文件有两部分组成Global Settings(全局参数设置）和Share Definitions（共享定义）组成。
    每个部分有消息头和参数构成，如[global]就是一个消息头，用[]标志。
    而参数的结构形式是parameter = value。
    注释用#表示，这个和shell脚本有点像
    而你会发现有一些前面有;号，这个表示这一行的配置可以更改，修改就要去掉;，让配置起作用。

五.Samba组成
    （1）Samba Global Settings 全局参数设置
          该部分由[global]段来完成配置，主要是设置整体的规则，有个参数一般要修改的是workgroup=mygroup，此句提供NT域名或者工作组名，是必须根据实际修改的。
    (2)Share Definitions 共享定义
          有很多段，都用[]标志开始的，这里要自己根据情况修改。

六.设置共享目录。
    反正随便设置一个目录给别人访问就行了，第一次配置，也就不考虑太多。
    $sudo mkdir -p /home/share/samba
    $sudo chmod 777 /home/share/samba

七.修改配置文件
    （1）global修改的地方，防止乱码产生
    [global]
    workgroup = WORKGROUP
    display charset = UTF-8
    unix charset = UTF-8
    dos charset = cp936
    （2）在文本最后添加Share段，其中/home/share/samba是共享目录
    [Share]
    comment = Shared Folder with username and password
    path = /home/share/samba
    public = yes
    writable = no
    valid users = user
    create mask = 0300
    directory mask = 0300
    force user = nobody
    force group = nogroup
    available = yes
    browseable = yes
    （3）搜索到security一项，修改如下
    security = user
    username map = /etc/samba/smbusers


八.定制Samba的用户
    在终端中输入一下命令
       $sudo useradd user        #增加了一个叫做user的用户
       $sudo smbpasswd user    #修改user的对samba服务的密码，系统会提示输入密码

九.重新启动服务
   保存并关闭配置文件，在终端中输入如下命令
    $sudo testparm
    重新启动服务
    $sudo /etc/init.d/samba restart

十.使用服务
    （1）在windows系统下使用
       方法一：在IE地址栏中输入： \\你的IP 然后回车，可能要求你输入用户名和密码，就是第八步所设定的。
       方法二：在网上邻居中新建邻居，在路径中输入: \\你的IP\Share 然后点击下一步完成，当然，还是可能会要求输入用户名和密码
    (2)在Linux下访问
       在终端中挂载文件系统
       $sudo mount -t smbfs -o username=user,password=123456 //218.*.*.*/Share /mnt
其中，-t参数指示了文件系统的类型，username是用户名，password是密码，218.*.*.*是你的IP，Share你在配置文件中已经指明的段名，/mnt是你要挂载所到的文件夹，当然你可以自己修改


