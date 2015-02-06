import mysql.connector
import time


def get_db_config ():
   config = {
     'user': 'root',
     'password': 'root',
     'host': '127.0.0.1',
     'database':'apireading',
     'raise_on_warnings': True}
   return config

def initialize_db():
    config = get_db_config()
    con = mysql.connector.connect(**config)
    cur = con.cursor()
    default_status = 0 # 0 = ready
    cur.execute('INSERT INTO current_instances (InstanceStatus) VALUES (%s)',(default_status,))
    print cur.lastrowid
    con.commit()
    con.close()
    return cur.lastrowid

#triggered when no dates are assigned, set's the current processID status back to 'ready'
def set_status_back_to_ready(process_id,cur,con):
    ready_status = 0
    cur.execute('UPDATE current_instances ' +
                'SET InstanceStatus = %s ' +
                'WHERE InstanceID = %s ', (ready_status, process_id))
    con.commit()

def get_date(process_id):
    config = get_db_config()
    con = mysql.connector.connect(**config)
    cur = con.cursor()
    
    
    while True:
        time.sleep(2)
        cur.execute('SELECT ReadingDate from date_table ' +
                'WHERE AssignedToInstanceID = ' + str(process_id) + ' ' +
                'AND ReadingDateStatus = 1 ' + 
                'ORDER BY ReadingDate asc ' +
                'Limit 1')
        rows = cur.fetchone()
        if rows == None:
            #re-initialize cursor, not sure why I have to do this, but it HAS to be done.
            con.close() 
            con = mysql.connector.connect(**config)
            cur = con.cursor()
            print "No Dates assigned"
            set_status_back_to_ready(process_id,cur,con)
        else:
            con.close()
            
            return rows[0]


def convert_time (reading_time):
       time_dict = {'12:00AM':1,
                '01:00AM':2,
                '02:00AM':3,
                '03:00AM':4,
                '04:00AM':5,
                '05:00AM':6,
                '06:00AM':7,
                '07:00AM':8,
                '08:00AM':9,
                '09:00AM':10,
                '10:00AM':11,
                '11:00AM':12,
                '12:00PM':13,
                '01:00PM':14,
                '02:00PM':15,
                '03:00PM':16,
                '04:00PM':17,
                '05:00PM':18,
                '06:00PM':19,
                '07:00PM':20,
                '08:00PM':21,
                '09:00PM':22,
                '10:00PM':23,
                '11:00PM':24}
       return time_dict[reading_time]


def get_reading_note (reading_value):

   defined_notes =["*","a","b","c","d","&"]

   if len(reading_value) == 0:
        return "0"
   
   last_char =  reading_value[-1]
   if last_char in defined_notes:
      return last_char
   else:
      return "0"

def get_reading_value_int (reading_value):

    value_length = len(reading_value)
    

    if reading_value.isdigit() :
        
        return reading_value
    else:
        new_value = reading_value[:(value_length -1)]
        if new_value.isdigit() :
            return new_value
        else:
            return "0"    
   
   

def write_list_to_db (datalist,current_url_date): #list of ApiReading objects to be written to database


    
    config = get_db_config()
    con = mysql.connector.connect(**config)
    cur = con.cursor()

    for ApiReading in datalist:
        cur.execute('''INSERT INTO readings (ReadingDate,
                                             ReadingTime,
                                             Region,
                                             ReadingValue,
                                             ReadingNote,
                                             ReadingValue_int
                                            )
                                            VALUES(%s,%s,%s,%s,%s,%s)''',
                                            (ApiReading.reading_date,
                                             convert_time(ApiReading.reading_time),
                                             ApiReading.region,
                                             ApiReading.reading_value,
                                             get_reading_note(ApiReading.reading_value),
                                             get_reading_value_int(ApiReading.reading_value))
                )
        #update list in current_instances & date_list
        cur.execute('''UPDATE date_table
                        SET ReadingDateStatus = 3
                        WHERE ReadingDate = %s''',(current_url_date,))
    con.commit() #all or nothing approach
    con.close()
