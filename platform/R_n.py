"""script used for evaluation of R_n"""

"""deprecated, updated formula on ETO.py file
"""

import T_mean
import math
import datetime


def Rs(Rs_umol_avg):
    "convert Rs in MJ/m^2"

    Rs_umol_tot = Rs_umol_avg*60*60*24
    Rs = Rs_umol_tot/4.6e6

    return Rs

def ea(T_min,T_max,RH_min,RH_max):
    et0_min = 0.618 * math.exp(17.27*T_min/(T_min+273.3))
    et0_max = 0.618 * math.exp(17.27 * T_max / (T_max + 273.3))

    ea = ((et0_min*RH_max) + (et0_max*RH_min))/100*2

    return ea


def Ra(julian_day=0,latitude=0.78):

    "specify the julian day, otherwise we automatically obtain get it (the current one)"
    if julian_day == 0:
        julian_day = datetime.datetime.now().day

    solar_declination = 0.409*math.sin(2*3.14*julian_day/365-1.39)
    inv_rel_dist = 1+0.033*math.cos(2*math.pi*julian_day/365)
    sunset_hour_angle = math.acos(-math.tan(latitude)*math.tan(solar_declination))
    Ra = 24*60/(math.pi*0.082*inv_rel_dist*(sunset_hour_angle)*math.sin(latitude)*math.sin(solar_declination)+math.cos(latitude)*math.cos(solar_declination)*math.sin(solar_declination))

    return Ra

def Rs0(Ra,altitude = 250):

    Rs0 = (0.075 + 0.00002*altitude)*Ra

    return Rs0

def Rn(Rs,ea=1,Rs0=1):

    t_mean, T_min, T_max = T_mean.T_mean('2021-3-24-0-0-10', '2021-3-24-0-30-10')
    Rns = (1-0.23)*Rs
    Rnl = 4.903e-09*(((T_min+273.16)**4+(T_max + 273.16)**4)/2)*(0.34-(0.14*(ea)**0.5))*(1.35*Rs/Rs0 - 0.35)
    Rn = Rns-Rnl

    return Rn