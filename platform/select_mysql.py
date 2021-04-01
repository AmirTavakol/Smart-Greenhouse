"""The following script aims at performing SELECT query to database in order to update
the JSON file (ET0_values.json) that is storing the informations related to the last measured values"""

#TODO
#add more parameter (Possibility to make specific select query (for date, only some element, keep n entries, etc...)
#TODO: possibility to estimate the mean value, max and minimum and so on...

import mysql.connector
from mysql.connector import errorcode
import datetime
import json
import db_connect



if __name__ == '__main__':
    # %% Connect to database, raise error if any
    mydb = db_connect.connect()


    mycursor = mydb.cursor()

    """
    now = datetime.datetime.now()
    select = "SELECT sensor, value, timestamp FROM sensorParser WHERE timestamp > '" + now.isoformat() + "'"
    """
    select = "SELECT sensor, value, timestamp FROM sensorParser WHERE timestamp > '2021-3-24-0-10-10' ORDER BY timestamp DESC LIMIT 6 "

    print(select)
    mycursor.execute(select)

    myresult = mycursor.fetchall()

    values= {} #dict containing all the values read from sensors

    for x in myresult:
        values[x[0]]=float(x[1]) #writing the dictionary
        print(x[2])

    timestamp = myresult[0][2] #timestamp

    with open('ET0_values.json') as json_file:
        data = json.load(json_file)

    data['values'] = values
    data['timestamp'] = timestamp.isoformat()
    json_file.close()


    with open('ET0_values.json', 'w') as outfile:
        json.dump(data, outfile, indent = 4)






