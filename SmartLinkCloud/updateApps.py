#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3
import urllib
import urllib2
import json
import types
import re


##-----------------------------------------------------------------------##

def get_pa_apps_fields(dbname):
    '''get fields from the pa_apps table'''

####################################################
##         connect the sqlite3 database           ##
####################################################

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    curs.execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'pa_apps' AND type = 'table'")
    for sql in curs.fetchone():
        #print sql
        fields_list = re.split(r',',sql)
        #fields_list = sql.split(',')
        #print fields_list

        pa_apps_fields_list = []

        pattern = re.compile('\w+')
        for pa_apps_fields in fields_list:
            #match = re.match(r'\w+',pa_apps_fields.lstrip())
            match = pattern.match(pa_apps_fields.lstrip())
            if match:
                #print match.group()
                pa_apps_fields_list.append(match.group())
        pa_apps_fields_list[0] = u'appid'
        print "---------------------pa_apps_fields_list--------------------------------"
        print pa_apps_fields_list
    curs.close()
    conn.close()

    return pa_apps_fields_list


##-----------------------------------------------------------------------##


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
    print "-------------------------------------URI----------------------------------------------"
    print URI

    req = urllib2.Request(URI)
    response = urllib2.urlopen(req)
    the_page = response.read()
    #the_page = response.read().decode('unicode-escape')
    print "---------------------------------the_page----------------------------------------------"
    print the_page
    json_dicts = json.loads(the_page, 'utf-8');
    print "---------------------------------json_dicts-----------------------------------------"
    print json_dicts

    curs.close()
    conn.close()

    #return order_dict_array
    return json_dicts
##-----------------------------------------------------------------------##

def update_all_apps(dbname,pa_apps_fields_list,json_dicts):
    '''update all apps'''

####################################################
##         connect the sqlite3 database           ##
####################################################

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    insert_lists= []

    for apps_info_dict in json_dicts:
        insert_list= []

        for key,value in apps_info_dict.items():
            if key in pa_apps_fields_list:
                if type(value) is types.UnicodeType:
                    insert_list.append(value.encode('utf-8'))
                else:
                    insert_list.append(value)
        insert_lists.append(insert_list)

    for app_list in insert_lists:
        print "############################insert_list##################################"
        for app_info in app_list:
            print "------------------------app_info-----------------------------"
            print app_info
####################################################
##  insert apps into  pa_apps table               ##
####################################################

    curs.execute("INSERT INTO pa_apps VALUES (?)",(terminalid,));

    conn.commit()


    curs.close()
    conn.close()

# def set_default_encoding():
#     import sys
#
#     print sys.getdefaultencoding()
#
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
#     print sys.getdefaultencoding()

##-----------------------------------------------------------------------##

if __name__ == '__main__':

    dbname = 'SmartLinkCloud.db'
    #set_default_encoding()
    pa_apps_fields_list = get_pa_apps_fields(dbname)
    json_dicts = get_all_apps(dbname)
    update_all_apps(dbname,pa_apps_fields_list,json_dicts)

