# Firmware compiling

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get clean

    sudo apt-get install gcc g++ binutils patch bzip2 flex bison make autoconf gettext texinfo unzip sharutils subversion libncurses5-dev ncurses-term zlib1g-dev

    mkdir openwrt
    cd openwrt

    svn checkout svn://svn.openwrt.org/openwrt/trunk
    cd trunk
    ./scripts/feeds update -a
    ./scripts/feeds install -a

# Errors

e4defrag.c:201:2: error: #error fallocate64 not available!
 #error fallocate64 not available!

