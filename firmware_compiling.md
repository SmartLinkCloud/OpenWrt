# Firmware compiling

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get clean

    sudo apt-get install gcc g++ binutils patch bzip2 flex bison make autoconf gettext texinfo unzip sharutils subversion libncurses5-dev ncurses-term zlib1g-dev

    mkdir openwrt
    cd openwrt

    svn checkout svn://svn.openwrt.org/openwrt/trunk
    cd trunk

    svn update

    cp feeds.conf.default feeds.conf
    
    sudo vim feeds.conf
add:
    src-git wifidog https://github.com/wifidog/wifidog-gateway.git
    
    ./scripts/feeds update -a
    ./scripts/feeds install -a

    make menuconfig
    sudo make V=99

# Errors

e4defrag.c:201:2: error: #error fallocate64 not available!
 #error fallocate64 not available!

