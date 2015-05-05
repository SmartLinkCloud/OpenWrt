#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('database')

print "Opened database successfully";

cursor = conn.execute("SELECT terminalid FROM pa_terminal")
for row in cursor:
   print "terminalid = ", row[0], "\n"

print "Operation done successfully";
conn.close()
