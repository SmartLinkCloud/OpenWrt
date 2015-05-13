#!/usr/bin/python

import sqlite3
import urllib
import urllib2
import json
import time
import os
##----------------------------------------------------------------------##

def updatePortalTemplate(dbname):
    '''update portal template'''

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

    update_portal_template_prefix_uri = "http://api1.juwan.cn/PhoneAssistantServer/template/getTerminalsTemplateUpload.php?terminalid=6


    updatetime_str = "&updatetime="

    updatetime_file = os.path.join(os.getcwd(),'update/protal_updatetime')

    with open(updatetime_file, 'r') as f:
        updatetime_version = f.read()
    # get the version of the current updatetime of the portal template from the version_file


    URI = update_portal_template_prefix_uri + terminalid + updatetime_str + updatetime_version
    # generate the URI to request
    print URI

    req = urllib2.Request(URI)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print the_page

    json_data = json.loads(the_page)


    ####################################################
    ## to judge if need to update portal template     ##
    ####################################################

    code = json_data['code']
    print "-----------code------------",code,type(code)

    if code == 'update':
        # if returned code == update , to update firmware
        print "portal template needs to update."
        updatetime = json_data['updatetime']
        download_url = json_data['downloadurl']
        portal_template_dir = os.path.join(os.getcwd(),'update/portal_updatetime')
        downloader(download_url,portal_template_dir)
        # download the new portal template

        os.system('unzip %s' % portal_template_dir)

        with open(updatetime_file, 'r') as f:
            f.wrtie(updatetime)
        # write the new updatetime to the portal_updatetime in update


    else:
        print "portal template is not need to update."

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
        updatePortalTemplate(dbname)

        time.sleep(24*3600)


