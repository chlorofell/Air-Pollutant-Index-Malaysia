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
entity_table= 'date_table' #entity table name--makes this generic 




def check_for_ready_instances():
    cnx = mysql.connector.connect(**config_with_db)
    cur = cnx.cursor()
    
    
    while True:
        time.sleep(1)
        cur.execute('SELECT InstanceID from current_instances ' +
                'WHERE InstanceStatus = 0 ' +
                'ORDER BY LastUpdateTimeStamp asc ' +
                'Limit 1')
        rows = cur.fetchone()
        if rows == None:
            #re-initialize cursor, not sure why I have to do this, but it HAS to be done.
            cnx.close() 
            cnx = mysql.connector.connect(**config_with_db)
            cur = cnx.cursor()
        else:
            cnx.close()
            
            return rows[0]
        
    
    
def assign_entities_to_instance(InstanceID,NumberOfEntities):

    assigned_status_inDB = 1
    
    cnx = mysql.connector.connect(**config_with_db)
    cur = cnx.cursor()

    for x in range(1,NumberOfEntities+1):
    
        cur.execute('SELECT ROWID FROM ' + entity_table + ' ' +
                    'WHERE ReadingDateStatus = 0 ' +
                    'ORDER BY ROWID asc ' +
                    'Limit 1')
        row = cur.fetchone() #row[0] is now the ROWID we need.
       
        cur.execute('UPDATE ' + entity_table + ' ' +
                    'SET AssignedToInstanceID = %s , ReadingDateStatus = %s ' + 
                    'WHERE ROWID =  %s', (InstanceID,assigned_status_inDB,row[0]))
        cnx.commit() #Have to commit everytime, otherwise select statement will pick the same row.

    cur2 = cnx.cursor()
    print InstanceID
    cur2.execute('UPDATE current_instances ' +
                'SET InstanceStatus = %s ' +
                'WHERE InstanceID = %s', (assigned_status_inDB,InstanceID))

    cnx.commit()
    cnx.close()
    
    
def main():

    NumberOfEntities = 3

    while True:
        time.sleep(1)
        CurrentInstanceID = check_for_ready_instances()
        if CurrentInstanceID == None:
            pass #do nothing and loop
        else:
            assign_entities_to_instance(CurrentInstanceID, NumberOfEntities) #currentinstanceID is something
        

if __name__ == "__main__":
    main()
    
