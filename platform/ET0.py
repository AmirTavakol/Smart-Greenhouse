"""Main Script used to perform ET0 evaluation"""
import json
import dbconnection
import ET0_evaluation
import math
import select_mysql
import R_n
import ast
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

"""
def delta(T_mean):
    '∆ slope vapour pressure curve [kPa °C-1]'
    #actually now we are passing T and not Tmean, we should work on this
    delta = 4098*(0.6108*math.exp(17.27*T_mean/(T_mean+237.3)))/((T_mean+237.3)**2) #formula  from excel file
    return delta

def gamma(atm_press):
    'psychrometric constant'
    gamma = 0.000665 * atm_press
    return gamma

with open('ET0_values.json') as json_file:
    data = json.load(json_file)
"""

def get(ET0):
    return ET0

if __name__ == '__main__':
    '''
    "first of all get the last measured values"
    select_mysql

    #loading measured values
    values = data['values']
    T = values['TC']
    atm_press = values['PRES']
    Rs = values['PAR']

    '''

    

    db = dbconnection.db_connection()
    file = db.getDataForParameter()
    try:
        dict = ast.literal_eval(file)
        Tmax = dict['max_tc']
        Tmin = dict['min_tc']
        RHmax = dict['max_hum']
        RHmin = dict['min_hum']
        par_avg = dict['avg_solar']

        print("Over the last 24h, the maximum temperature was: " + str(Tmax) +"\n the minimum temperature was: "+ str(Tmin)+ " \n while RH minimum: "+str(RHmin)+" and RH Maximum: "+ str(RHmax) +" \n the average solar radiation was:" + str(par_avg))

        values = db.getDataLastEpoch()
        atm_press = float(values[8][1])/1000
        julian_day = values[8][2].timetuple().tm_yday
        print(atm_press)

        measurement = ET0_evaluation.measurement(Tmin, Tmax, RHmin, RHmax, atm_press, par_avg, julian_day = julian_day)

        """
        Rs = R_n.Rs(Rs_umol_avg=par_avg)
        ea = R_n.ea(T_min=Tmin,T_max=Tmax,RH_min=RHmin,RH_max=RHmax)
        Ra = R_n.Ra(julian_day=0,latitude=0.70) #julian day setted to zero means that it automatically estimate it.
        #TODO modify the latitude accordingly or get it from somewhere
        #TODO as above, get the altitude from somewhere
        Rs0 = R_n.Rs0(Ra=Ra,altitude=200)
        Rn = R_n.Rn(Rs=Rs, ea=ea,Rs0 = Rs0)
        T_mean = Tmax+Tmin/2
        print("The estimated Rn is " + str(Rn))
        """


        #delta = delta(T_mean)
        #gamma = gamma(atm_press/100)
        pprint(vars(measurement))
        print("ea :", measurement.ea)
        print("Rs :", measurement.Rs)
        print("Rs0 :", measurement.Rs0)
        print("Rn :", measurement.Rn)
        print("Ra :", measurement.Ra)
        print("Delta :", measurement.delta)
        print("gamma :", measurement.gamma)

        #print(measurement.__dict__)


        ET0 = measurement.ET_0
        print('\n ET0 ', ET0)

        db.saveET0Value(ET0)

        #make the insert call here
    except:
        print("cannot retrieve data from database")


# points = 200
# et0s = np.zeros(points)

# for i in range(points):
#
#     measurement = ET0_evaluation.measurement(Tmin, Tmax, RHmin, RHmax, atm_press, par_avg, julian_day=julian_day)
#     et0s[i] = measurement.ET_0
#
#
# plt.plot(et0s)
# plt.show()







