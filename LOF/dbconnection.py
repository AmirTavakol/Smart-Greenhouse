from mysql.connector import MySQLConnection, Error
import mysql
import cherrypy

class db_connection(object):

    def __init__(self):
        self.user= 'root'
        self.password= 'Qwertykk.22!'
        self.host = '80.210.98.95'
        self.database = 'MeshliumDB'
        self.port = 6606

    def call_procedure(self, procedure_name, args =[], parameter = False):
        """ Connect to MySQL database """
        res = []
        try:
            print('Connecting to MySQL database.')
            conn = mysql.connector.connect(host=self.host,
                                         database=self.database,
                                         user=self.user,
                                         password=self.password,
                                         port=self.port
                                         )

            if conn.is_connected():
                print('connection established.')
                try:
                    cursor = conn.cursor()
                    result = cursor.callproc(procedure_name, args)
                    conn.commit()
                except mysql.connector.errors.IntegrityError:
                    print('HTTP:409, Duplicate User ERROR')
                    raise cherrypy.HTTPError(409, "User Details are duplicated")
                
                if(parameter):
                    cursor.close()
                    conn.close()
                    print("connection closed")
                    return result
                else:
                    for result in cursor.stored_results():
                        data = result.fetchall()
                        res.extend(data)
                        cursor.close()
                        conn.close()
                        print("connection closed")
                return res
            else:
                print('connection failed.')
                return 0

        except Error as error:
            print(error)
            return 0

    #method to get data for some duration of hours
    def getSensorData(self, duration = 8):
        arg = [duration]
        response = self.call_procedure(procedure_name='USP_GET_SENSOR_DATA', args=arg)
        return response

    #method to get most recent data
    def getDataLastEpoch(self):
        response = self.call_procedure(procedure_name='USP_GET_DATA_LAST_EPOCH')
        return response

    #method to get data for parameter estimation returns a json in format:
    #{"max_tc": 31.970, "min_tc": 14.670, "max_hum": 63.100, "min_hum": 17.200, "avg_solar": 76.702}
    def getDataForParameter(self):
        arg = list([0])
        response = self.call_procedure(procedure_name='USP_GET_PARAMETER_DATA', args = arg, parameter = True)
        return response[-1]



