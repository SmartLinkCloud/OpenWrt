#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3
import urllib
import urllib2
import json
import re
import time

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
    print "---------------------------------the_page----------------------------------------"
    print the_page
    json_dicts = json.loads(the_page, 'utf-8');
    print "---------------------------------json_dicts---------------------------------------"
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

####################################################
##  generate the insert_lists for insert          ##
####################################################

    insert_lists= []
    for apps_info_dict in json_dicts:
        insert_list= []
        for field in pa_apps_fields_list:
            insert_list.append(apps_info_dict[field])
        insert_lists.append(insert_list)

    print "---------------------insert_lists-------------------"
    print insert_lists

####################################################
##         return appids in pa_apps               ##
####################################################
    appid_list = []

    curs.execute("SELECT appid FROM pa_apps")
    for appid in curs.fetchall():
        print "------------------appid-----------------",appid
        appid_list += appid
        #generate appid list
    print "---------------------appid_list-------------"
    print appid_list

####################################################
##  insert apps into  pa_apps table               ##
####################################################

    for app_list in insert_lists:
        print "############################insert_list##################################"
        #judge if need to insert into pa_apps
        #print "-----------------app_list[0]-------------------",app_list[0],app_list[0] == appid_list[0],type(app_list[0]),type(appid_list[0])
        if int(app_list[0]) in appid_list:
            # convert unicode to int
            print "already has this app,don't need to insert"
        else:
            curs.execute("INSERT INTO pa_apps VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",tuple(app_list));
            print "insert new app_info into pa_apps"
        # for app_info in app_list:
        #     print "------------------------app_info-----------------------------"
        #     print app_info.encode('utf-8')

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
    while 1:

        json_dicts = get_all_apps(dbname)
        update_all_apps(dbname,pa_apps_fields_list,json_dicts)
        time.sleep(15)
