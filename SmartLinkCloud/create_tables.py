#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('SmartLinkCloud.db')

print "Opened database successfully";

conn.execute('''CREATE TABLE pa_terminal(terminalid TEXT(8) NOT NULL);''')
print "Table created pa_terminal successfully";

conn.execute('''CREATE TABLE pa_apps(
        appid INTEGER NOT NULL,
        serverid TEXT(4),
        appname  TEXT(8),
        style  INTEGER,
        packagename  TEXT(8),
        version  TEXT(4),
        downloadurl  TEXT(32),
        images  TEXT(32),
        size  INTEGER(8),
        downloads  INTEGER,
        score  INTEGER,
        systemreq  TEXT(8),
        classificationid  INTEGER,
        sortid  INTEGER,
        developer  TEXT,
        shortdesc  TEXT,
        details  TEXT,
        updatetime2  TEXT(8),
        dropflg  INTEGER,
        bbei  INTEGER,
        bbeisortid  INTEGER,
        jwbz  INTEGER,
        cmbb  INTEGER,
        cmbbsortid  INTEGER
        );''')
print "Table created pa_apps successfully";

conn.execute('''CREATE TABLE "pa_statistics"(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        appid  INTEGER NOT NULL,
        addtime  TEXT,
        terminalid  TEXT(8),
        updateflg  INTEGER,
        mac  TEXT(8),
        imei  TEXT(8),
        model  TEXT(8),
        imsi  TEXT(8),
        identification  TEXT(8)
        );''')
print "Table created pa_statistics successfully";

conn.execute('''CREATE UNIQUE INDEX appid ON pa_apps('appid');''')
print "UNIQUE INDEX created appid successfully";

conn.commit()

conn.close()
