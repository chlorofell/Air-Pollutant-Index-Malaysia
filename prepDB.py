import sys
from datetime import date, timedelta as delta_time
import time
import mysql.connector


config_with_db = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database' : 'apireading',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config_with_db)
cur = cnx.cursor()

d1 = date(2015,1,16) #statt Date yyyy,mm,dd
d2 = date(2015,2,5) #end Date yyyy,mm,dd
delta = d2 - d1

default_status = 0 

for i in range(delta.days + 1):
    current_url_date = str(d1 + delta_time(days=i))
    print current_url_date
    cur.execute('''INSERT INTO date_table (ReadingDate,ReadingDateStatus)
                                            VALUES(%s,%s)''',
                                            (current_url_date,
                                             default_status))

cnx.commit()
cnx.close()
