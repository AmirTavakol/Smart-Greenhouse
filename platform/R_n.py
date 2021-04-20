"""script used for evaluation of R_n"""

#TODO: fix evaluation of ea and Rs0

import T_mean
import math
import datetime

def ea(T_min,T_max,RH_min,RH_max):
    et0_min = 0.618 * math.exp(17,27*T_min/(T_min+273.3))
    et0_max = 0.618 * math.exp(17, 27 * T_max / (T_max + 273.3))

    ea = ((et0_min*RH_max) + (et0_max*RH_min))/100*2

    return ea


def Ra(julian_day=0,latitude):

    "specify the julian day, otherwise we automatically obtain get it (the current one)"
    if julian_day == 0:
        julian_day = datetime.datetime.now().day

    solar_declination = 0.409*math.sin(2*math.pi()*julian_day/365-1.39)
    inv_rel_dist = 1+0.033*math.cos(2*math.pi*julian_day/365)
    Ra = 24*60/(math.pi*0.082*inv_rel_dist*(sunset_hour_angle)*math.sin(latitude)*math.sin(solar_declination)+math.cos(latitdue)*math.cos(solar_declination)*math.sin(solar_declination))

    return Ra

def Rs0(Ra,altitude = 200):

    Rs0 = (0.075 + 0.00002*altitude) * Ra

    return Rs0

def R_n(Rs,ea=1,Rs0=1):

    t_mean, T_min, T_max = T_mean.T_mean('2021-3-24-0-0-10', '2021-3-24-0-30-10')
    Rns = (1-0.23)*Rs
    Rnl = 4.903e-09*(((T_min+273.16)**4+(T_max + 273.16)**4)/2)*(0.34-(0.14*(ea)**0.5))*(1.35*Rs/Rs0 - 0.35)
    Rn = Rns-Rnl

    return Rn