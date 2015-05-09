#!/usr/bin/python

import sqlite3
import urllib
import urllib2
import json
import time
import os
##----------------------------------------------------------------------##

def askWIFI(dbname,):
    '''upload terminal information to server'''

    ####################################################
    ##         connect the sqlite3 database           ##
    ####################################################

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    ####################################################
    ##  retuen the terminalid from  pa_terminal table ##
    ####################################################

    curs.execute("SELECT terminalid FROM pa_terminal")
    terminalid = curs.fetchone()[0]

    print "Now, terminal id is: " + terminalid

    ask_wifi_prefix_uri = "http://api1.juwan.cn/PhoneAssistantServer/template/ask_wifi.php?terminalid="
    version_str = "&version="

    version_file = os.path.join(os.getcwd(),'update/version')

    with open(version_file, 'r') as f:
        firmware_version = f.read()
    # get the version of the current firmware

    URI = ask_wifi_prefix_uri + terminalid +version_str + firmware_version
    # generate the URI to request
    print URI

    req = urllib2.Request(URI)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print the_page

    json_data = json.loads(the_page)
    code = json_data['code']
    print "-----------code------------",code,type(code)

    if code == '1':
        print "upload terminal information successfully."
    else:
        print "upload terminal information unsuccessfully."

    curs.close()
    conn.close()

##----------------------------------------------------------------------##

if __name__ == '__main__':

    dbname = 'SmartLinkCloud.db'

    while 1:
        askWIFI(dbname)

        time.sleep(15*60)


