#Erors:

/usr/lib/git-core/git-pull: exec: line 1: git-merge: not found

 a git pull fails on git-merge not found.

 Caused by:
 links under /usr/libexec/git-core/ are broken, refer to git in the current dir.

 Workaround:
 Create a link to git in /usr/libexec/git-core/
#waring

ln -s $(which git) /usr/lib/git-core worked here to fix it on trunk
