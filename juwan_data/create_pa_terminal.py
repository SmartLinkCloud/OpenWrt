#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('database')

print "Opened database successfully";

conn.execute('''CREATE TABLE pa_terminal
       (terminalid VARCHAR NOT NULL);''')
print "Table created successfully";

conn.close()
