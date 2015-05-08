#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3
import urllib
import urllib2
import json
import re
import time
import os

##-----------------------------------------------------------------------##

def getPaAappsFields(dbname):
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


def getAllApps(dbname):
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

    return json_dicts

##-------------------------------------------------------------------------##

def insertList(json_dicts,pa_apps_fields_list):
    insert_lists= []
    for apps_info_dict in json_dicts:
        insert_list= []
        for field in pa_apps_fields_list:
            insert_list.append(apps_info_dict[field])
        insert_lists.append(insert_list)

    print "---------------------insert_lists-------------------"
    print insert_lists

    return insert_lists


##-------------------------------------------------------------------------##

def fileDir(app_list):
    '''generate file dir and basename'''

    url = app_list[6]
    print "------------------------------url-----------------------------"
    print url

    basename = os.path.basename(url)

    path = os.path.join(os.getcwd(),'pa_apps',app_list[0])
    os.makedirs(path)
    file_dir = os.path.join(path,basename)
    print "-------------------------fileDir----------------------------"
    print file_dir

    return file_dir

##-----------------------------------------------------------------------##

def downloadZip(url,file_dir):
    '''download zip useing urllib2,supports continue transferring from breakpoint'''
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




##-------------------------------------------------------------------------##

def updateAllApps(dbname,insert_lists):
    '''update all apps'''

####################################################
##         connect the sqlite3 database           ##
####################################################

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

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
            conn.commit()
            print "------------insert new app_info into pa_apps------------------"

####################################################
##  download the zip using urllib2                ##
####################################################

            url = app_list[6]
            file_dir = fileDir(app_list)
            downloadZip(url,file_dir)

    curs.close()
    conn.close()

##-----------------------------------------------------------------------##

if __name__ == '__main__':

    dbname = 'SmartLinkCloud.db'
    pa_apps_fields_list = getPaAappsFields(dbname)

    while 1:

        json_dicts = getAllApps(dbname)
        insert_lists = insertList(json_dicts,pa_apps_fields_list)
        updateAllApps(dbname,insert_lists)
        time.sleep(15*60)
