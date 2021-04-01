import mysql.connector
from mysql.connector import errorcode

def connect():
    # %% Connect to database, raise error if any
    try:
        mydb = mysql.connector.connect(user='sslroot',
                                       password='idrom3sh..',
                                       host='80.210.98.95',
                                       database='MeshliumDB')

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return mydb