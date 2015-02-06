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

data_list = ["123*","3*","23a","24d","351&","#","0","","bacik/"]

for string in data_list:
    print string + " : " + str(get_reading_value_int(string)) + " , " + str(get_reading_note(string))

