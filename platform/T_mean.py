"""Function to evaluate the mean of a feature (such as the temperature) over a specified time interval (for instance 24h in P-M formula)

"""
#####EXAMPLE########
#Mean('2021-3-24-0-0-10', '2021-3-24-0-30-10')

import db_connect

def Mean(start, end, sensor = 'TC'):

    mydb = db_connect.connect()
    mycursor = mydb.cursor()
    select = "SELECT value FROM sensorParser WHERE (timestamp > '"+ start +"' AND timestamp < '"+ end + "' AND sensor = '"+ sensor +"') ORDER BY value"
    mycursor.execute(select)

    myresult = mycursor.fetchall()
    T_max = myresult[-1]
    T_min= myresult[0]
    T_mean = (T_min + T_max)/2

    return T_mean,T_min, T_max








