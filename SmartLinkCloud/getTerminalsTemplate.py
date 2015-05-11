#!/usr/bin/python

import sqlite3
import urllib
import urllib2
import json
import time
import os
##----------------------------------------------------------------------##

def updateFirmware(dbname):
    '''update firmware version'''

    ####################################################
    ##         connect the sqlite3 database           ##
    ####################################################

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    ####################################################
    ##  get terminalid,serial number,firmware version ##
    ####################################################

    curs.execute("SELECT terminalid FROM pa_terminal")
    terminalid = curs.fetchone()[0]

    print "Now, terminal id is: " + terminalid

    update_firmware_prefix_uri = "http://houtai.juwan.cn/PhoneAssistantServer/template/getUpdate_jwbox.php?terminalid="

    serial_number_str = "&serial_number="
    serial_number = "???"

    version_str = "&version="

    version_file = os.path.join(os.getcwd(),'update/version')

    with open(version_file, 'r') as f:
        firmware_version = f.read()
    # get the version of the current firmware from the version_file


    URI = update_firmware_prefix_uri + terminalid + serial_number_str + serial_number + version_str + firmware_version
    # generate the URI to request
    print URI

    req = urllib2.Request(URI)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print the_page

    json_data = json.loads(the_page)


    ####################################################
    ## to judge if need to update firmware            ##
    ####################################################

    code = json_data['code']
    print "-----------code------------",code,type(code)

    if code == 'update':
        # if returned code == update , to update firmware
        print "firmware need to update."
        version = json_data['version']
        download_url = json_data['downloadurl']
        firmware_dir = os.path.join(os.getcwd(),'update/firmware')
        downloader(download_url,firmware_dir)
        # download the new firmware
        with open(version_file, 'r') as f:
            f.wrtie(version)
        # write the new verison to the version_file in update

        ##---to do :install the firmware

    else:
        print "firmware is not need to update."

    curs.close()
    conn.close()

##----------------------------------------------------------------------##

def downloader(url,file_dir):
    '''download firmware useing urllib2,supports continue transferring from breakpoint'''
    req = urllib2.Request(url)
    #req.add_header('Range', 'bytes=0-20')
    # set the range, from 0byte to 19byte, 20bytes len
    # continue transferring from breakpoint
    res = urllib2.urlopen(req)

    data = res.read()

    print data
    print '----urlib2 downloading start-----'
    print 'len:%d'%len(data)

    with open(file_dir,'wb') as downloader:
        downloader.write(data)

##----------------------------------------------------------------------##

if __name__ == '__main__':

    dbname = 'SmartLinkCloud.db'

    while 1:
        updateFirmware(dbname)

        time.sleep(24*3600)


