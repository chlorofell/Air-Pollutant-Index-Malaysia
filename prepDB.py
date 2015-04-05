import sys
from datetime import date, timedelta as delta_time
import time
import mysql.connector
from datetime import datetime

config_with_db = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database' : 'apireading',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config_with_db)
cur = cnx.cursor()
default_status = 0

#get-last-date-from-db
cur.execute('SELECT MAX(ReadingDate) from date_table ')
rows = cur.fetchone()
last_date_in_db =  rows[0]

#get number of 
todaysdate = date.today()
delta = todaysdate - last_date_in_db

#insert-up-to-current-date 
for i in range(delta.days-1): #current date not taken, data for today is still being collected, so we'll skip today, and leave it for tomorrow.
    current_url_date = str(last_date_in_db + delta_time(days=(i+1)))
    print current_url_date
    cur.execute('''INSERT INTO date_table (ReadingDate,ReadingDateStatus)
                                            VALUES(%s,%s)''',
                                            (current_url_date,
                                             default_status))

cur.execute('''DELETE from current_instances ''')

cnx.commit()
cnx.close()
