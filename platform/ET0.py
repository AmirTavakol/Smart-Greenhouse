import json
import ET0_evaluation
import math

def delta(T_mean):
    '∆ slope vapour pressure curve [kPa °C-1]'
    #actually now we are passing T and not Tmean, we should work on this
    delta = 4098*(0.6108*math.exp(17.27*T_mean/(T_mean+237.3)))/((T_mean+237.3)**2) #formula copied from excel file
    return delta

def R_n():
    'net radiation'
    R_n = 1 #set to one to avoid error now
    #can we directlty measure this (net radiation) instead of measure it?
    return R_n

def gamma(atm_press):
    'psychrometric constant'
    gamma = 0.000665 * atm_press
    return gamma

with open('ET0_values.json') as json_file:
    data = json.load(json_file)


if __name__ == '__main__':

    #loading measured values
    values = data['values']
    T = values['temperature']
    atm_press = values['Atm Pressure']

    #evalauting coefficients
    delta = delta(T)
    gamma = gamma(atm_press)
    R_n = R_n()


    print(values)
    ET0 = ET0_evaluation.ET0(delta, R_n, gamma, T)

    print(ET0)




