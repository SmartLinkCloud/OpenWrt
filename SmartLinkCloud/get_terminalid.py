#!/usr/bin/python

import sqlite3
import urllib
import urllib2

conn = sqlite3.connect('SmartLinkCloud.db')
print "Opened database successfully";

curs = conn.cursor()
curs.execute("SELECT terminalid FROM pa_terminal")
for row in curs.fetchall():
    print row[0]

result = conn.execute('select count(*) from pa_terminal')
count = result.fetchone()[0]
print "rowcount = ",count

def get_local_mac_address():
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

def get_local_MAC_ADDRESS():
    MAC = get_local_mac_address().upper()
    MAC_ADRESS = ":".join([MAC[e:e+2] for e in range(0,11,2)])
    return MAC_ADRESS

def get_ip_address(ifname):
    import socket
    import fcntl
    import struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

    return ip

print "local mac address is : " + get_local_mac_address()
print "local MAC ADDRESS is : " + get_local_MAC_ADDRESS()
print "lo ip is : " + get_ip_address('lo')
print "eth1 ip is : " + get_ip_address('eth1')

URI = "http://api1.juwan.cn/PhoneAssistantServer/template/getTerminalInfo.php?mac=" + get_local_mac_address()
print URI

if count > 0:
    pass
else:
    req = urllib2.Request(URI)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print the_page

print "Operation done successfully";
conn.close()


