#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3
import urllib
import urllib2
import json
import types

def get_all_apps(dbname):
    '''get all apps'''

####################################################
##         connect the sqlite3 database           ##
####################################################

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

####################################################
##     get terminalid from  the pa_terminal table ##
####################################################

    curs.execute("SELECT terminalid FROM pa_terminal")
    for row in curs.fetchall():
        print "Now, terminal id is: " + row[0]
        terminalid = row[0]

    get_apps_prefix_uri = "http://houtai.juwan.cn/PhoneAssistantServer/template/getAllApps_jwbox.php?terminalid="
    URI = get_apps_prefix_uri + terminalid
    print URI

    req = urllib2.Request(URI)
    response = urllib2.urlopen(req)
    the_page = response.read()
    #the_page = response.read().decode('unicode-escape')

    print "\n"
    print "-json-#-"*10
    print "\n"
    print the_page
    print "\n"

    from collections import OrderedDict
    order_dict_array = json.loads(the_page, object_pairs_hook=OrderedDict);
    print order_dict_array

    for order_dicts in  order_dict_array:
        for key,value in order_dicts.items():
            print "\n"
            print "-"*50
            print type(value)
            print "\n"
            if type(value) is types.UnicodeType:
                print 'key=',key,'，value=',value.encode('utf-8')
            else:
                 print 'key=',key,'，value=',value

####################################################
##  insert apps into  pa_apps table ##
####################################################

    #    curs.execute("INSERT INTO pa_apps VALUES (?)",(terminalid,));

     #   conn.commit()


    curs.close()
    conn.close()

#def set_default_encoding():
#    import sys
#
#    print sys.getdefaultencoding()
#
#    reload(sys)
#    sys.setdefaultencoding('utf-8')
#    print sys.getdefaultencoding()
#
#    print u'\u6ce8\u91ca'.encode('utf-8')

if __name__ == '__main__':

    dbname = 'SmartLinkCloud.db'
    #set_default_encoding()
    get_all_apps(dbname)

