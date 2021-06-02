"""Function to evaluate the mean of a feature (such as the temperature) over a specified time interval (for instance 24h in P-M formula)

"""
#####EXAMPLE########
#T_mean('2021-3-24-0-0-10', '2021-3-24-0-30-10')

import db_connect

def T_mean(start, end, sensor = 'TC'):

    mydb = db_connect.connect()
    mycursor = mydb.cursor()
    select = "SELECT value FROM sensorParser WHERE (timestamp > '"+ start +"' AND timestamp < '"+ end + "' AND sensor = '"+ sensor +"') ORDER BY value"
    mycursor.execute(select)

    myresult = mycursor.fetchall()
    T_max = float(myresult[-1][0])
    T_min= float(myresult[0][0])

    T_mean = (T_min + T_max)/2

    return T_mean,T_min, T_max




t_mean, T_min, T_max = T_mean('2021-5-21-0-0-00', '2021-5-22-0-0-00')

print(T_min, T_max)



