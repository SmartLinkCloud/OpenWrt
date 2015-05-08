#!/usr/bin/python

import sqlite3
import urllib
import urllib2
import json

##----------------------------------------------------------------------##

def getLocalMacAddress():
    '''get local mac address'''
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

##----------------------------------------------------------------------##

def getLocalMACADDRESS():
    '''get local MAC ADDRESS,upper mac address with the colon'''
    MAC = getLocalMacAddress().upper()
    MAC_ADRESS = ":".join([MAC[e:e+2] for e in range(0,11,2)])
    return MAC_ADRESS

##----------------------------------------------------------------------##

def getIpAddress(ifname):
    '''get ip_address,use it need ifname,for example :'eth1'.'''
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

##----------------------------------------------------------------------##

def getTerminalId(dbname,mac):
    '''get terminal id from pa_terminal'''

    get_terminal_id_prefix_uri = "http://api1.juwan.cn/PhoneAssistantServer/template/getTerminalInfo.php?mac="
    URI = get_terminal_id_prefix_uri + mac
    print URI

####################################################
##         connect the sqlite3 database           ##
####################################################

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

####################################################
##  retuen the row count of the pa_terminal table ##
####################################################

    result = curs.execute('select count(*) from pa_terminal')
    count = result.fetchone()[0]
    print "rowcount = ",count

    if count > 0:
        print "Already has terminalid"
    else:
        req = urllib2.Request(URI)
        response = urllib2.urlopen(req)
        the_page = response.read()

        print the_page

        json_data = json.loads(the_page)
        terminalid = json_data['terminalid']
        print "terminalid in the jsondata is : " + terminalid

####################################################
##  insert terminalid into  pa_terminal table ##
####################################################

        curs.execute("INSERT INTO pa_terminal VALUES (?)",(terminalid,));

        conn.commit()

    curs.execute("SELECT terminalid FROM pa_terminal")
    for row in curs.fetchall():
        print "Now, terminal id is: " + row[0]

    curs.close()
    conn.close()

##----------------------------------------------------------------------##

if __name__ == '__main__':

    dbname = 'SmartLinkCloud.db'

    print "local mac address is : " + getLocalMacAddress()
    print "local MAC ADDRESS is : " + getLocalMACADDRESS()
    print "lo ip is : " + getIpAddress('lo')
    print "eth1 ip is : " + getIpAddress('eth1')

    mac = getLocalMacAddress()
    getTerminalId(dbname,mac)

