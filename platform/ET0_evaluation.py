'This script contains the formula for the evaluation of ET0 in both cases (wind = 0, wind >0)'
from typing import Any, Union

"""script used for evaluation of R_n"""

import T_mean
import math
import datetime

class measurement(object):

    def __init__(self, Tmin, Tmax, RHmin,
                 RHmax, atm_pressure, par_avg,
                 julian_day = 0, latitude = 0.7834, altitude = 232, wind = 0):
        self.Tmin = Tmin
        self.Tmax = Tmax
        self.RHmin = RHmin
        self.RHmax = RHmax
        self.atm_pressure = atm_pressure
        self.T_mean = (Tmax + Tmin )/2
        self.julian_day = julian_day
        self.par_avg = par_avg
        self.latitude = latitude
        self.altitude = altitude
        self.wind = wind
        self.ET_0 = self.ET0()

        """
        self.gamma = self.gamma()
        self.ea = self.ea()
        self.Rs = self.Rs()
        self.Ra = self.Ra()
        self.Rs0 = self.Rs0()
        self.Rn = self.Rn()
        """


    @property
    def ea(self):
        T_min = self.Tmin
        T_max = self.Tmax
        RH_min = self.RHmin
        RH_max = self.RHmax
        et0_min = 0.618 * math.exp((17.27*T_min)/(T_min+237.3))
        et0_max = 0.618 * math.exp((17.27 * T_max) / (T_max + 237.3))

        ea = ((et0_min*RH_max) + (et0_max*RH_min))/200
        return ea

    @property
    def Rs(self):
        "convert Rs in MJ/m^2"
        Rs_umol_avg = self.par_avg
        Rs_umol_tot = Rs_umol_avg*60*60*24
        Rs = Rs_umol_tot/(2.02*1e6)

        return Rs

    @property
    def Ra(self):
        julian_day = self.julian_day
        latitude = self.latitude
        "specify the julian day, otherwise we automatically obtain get it (the current one)"
        if julian_day == 0:
            julian_day = datetime.datetime.now().day

        solar_declination = 0.409*math.sin(2*3.14*julian_day/365-1.39) #OK
        inv_rel_dist = 1+0.033*math.cos(2*math.pi*julian_day/365) #OK
        sunset_hour_angle = math.acos(-math.tan(latitude)*math.tan(solar_declination)) #OK
        Ra = 24*60/math.pi*0.082*inv_rel_dist * (sunset_hour_angle * math.sin(latitude)*math.sin(solar_declination) + math.cos(latitude) * math.cos(solar_declination) * math.sin(sunset_hour_angle)) #should be OK
        return Ra

    @property
    def Rs0(self):

        Ra = self.Ra
        altitude = self.altitude
        Rs0 = (0.75 + 0.00002*altitude)*Ra #OK
        return Rs0

    @property
    def Rn(self):

        Rs = self.Rs
        ea = self.ea
        Rs0 = self.Rs0
        T_max = self.Tmax
        T_min = self.Tmin

        #t_mean, T_min, T_max = T_mean.T_mean('2021-3-24-0-0-10', '2021-3-24-0-30-10') deprecated old method
        Rns = (1-0.23)*Rs
        Rnl = 4.903e-09 * (((T_min+273.16)**4+(T_max + 273.16)**4)/2) * (0.34 - (0.14 * ea ** 0.5)) * (1.35 * Rs / Rs0 - 0.35)
        Rn = Rns-Rnl

        return Rn

    @property
    def delta(self):
        '∆ slope vapour pressure curve [kPa °C-1]'
        T_mean = self.T_mean
        # actually now we are passing T and not Tmean, we should work on this
        delta = 4098 * (0.6108 * math.exp(17.27 * T_mean / (T_mean + 237.3))) / (
                    (T_mean + 237.3) ** 2)  # formula  from excel file

        return delta

    @property
    def gamma(self):
        'psychrometric constant'
        atm_press= self.atm_pressure
        gamma= 0.000665 * atm_press

        return gamma


    def ET0(self, es=0, G=0):

        gamma = self.gamma
        delta = self.delta
        R_n = self.Rn
        T = self.T_mean
        wind = self.wind
        ea = self.ea

        if wind == 0:
            #complete formula for wind =!= 0
            ET = (0.408 * delta * (R_n - G))/(delta + gamma)
        else:
            ET = (0.408 * delta * (R_n - G) + (gamma * (900/(T+273)) * wind *(es - ea)))/(delta + gamma*(1 + (0.34*wind)))


        self.ET_0 = ET

        return ET

    def set_julian_day(self, julian_day):
        self.julian_day = julian_day

