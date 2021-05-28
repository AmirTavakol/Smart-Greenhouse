import dbconnection
import db_connect
from datetime import date
import ast
import json


db = dbconnection.db_connection()
try:
    Et0 = float(db.getET0Value()[0][0])
except:
    print("cannot retrieve Evapotranspiration from database")
#at this point we need to evaluate etc.

try:
    """ INSERT HERE THE QUERY FOR DB TO GET THE CROP ID AND THE SEEDING TIME"""
    crop_id = 1 #TODO: from db
    seeding_date = date(2021, 5, 2) #TODO: from db
    current_date = date.today()

    seeded = current_date - seeding_date
    seeded = seeded.days
    crop_type = "basil"  # TODO: from db

except:
    print("something wrong retrieving json from database")



try:
    path_json_file = 'Greenhouse/Smart-Greenhouse/platform/' + crop_type +'.json'
    file = open(path_json_file)
    data = json.load(file)
    kcb = data['Kcb'] #constant for Etc. It depends on the crop type and age
    #h = data['height']  #  height is not used anymore, look below for further details
    periods = data['periods']
except:
    print("Json file related to the crop not found")


#print(data['Kcb'])

try:
    current_stage = '' # this is the current stage of the plant {initial, middle, final}
    if seeded >= periods['end']:
        current_stage = 'end'
    elif (seeded >= periods['mid'] & seeded < periods['end']):
        current_stage = 'mid'
    elif (seeded >= periods['ini'] & seeded < periods['mid']):
        current_stage = 'ini'
    else:
        print("wrong seeded time, I will set the 'stage' as 'mid'")

except:
    print("error detecting the stage")

#getting the height of the plants

"""We will not focus on the height of the plants, we are considering Kc values already calibrated for basil so it is not 
required to evaluate it, Maybe if some group a day will work more on this, can also change it, so I will keep the part of
code I already wrote for this."""

# try:
#     h = h[current_stage]
#     if current_stage == 'ini':
#         h = ....
# try:
#     RHmin = ast.literal_eval(db.getDataForParameter())['min_hum']
#     #corerction factor for Kcb
#     correction_factor = -0.08 - 0.004 * (RHmin - 45) * (h[current_stage] / 3) ** 0.3
# except:
#     print("cannot retrieve data from database, hence it is not possible to evaluate the correction factor for Kcb ")
#
# try:
#     #now we need to calibrate them in base of our actual environmental conditions
#     if current_stage == 'ini':
#         Kcb = kcb[current_stage]
#         #here modify the height as well... if you are in the initial phase, the height is not constant, multiply it by a factor depending on the day
#
#     else:
#         Kcb = kcb[current_stage] + correction_factor
#

#
# #print('Kcb = ',Kcb)
#
# #now let's think to Ke
# try:
#     kr = 0.9 #set equal to 0.9 for sake of semplicity, if you have time modify it accordingly with page 145 (really time expensive)
#     Kcmax = min(1.2+correction_factor, Kcb + 0.5)
#
#     #print('Kcmax = ', Kcmax)
#
#     Ke = kr * (Kcmax - Kcb)
#
#     #print("Ke = ", Ke)
#
#     Kc = Ke + Kcb

try:
    Kc = kcb[current_stage]

    Etc = Et0 * Kc
    print("with the current Kc = ", Kc, 'the resulting Etc is ', Etc)
except:
    print(" cannot evaluate kc")

"""following lines of code can be used if you want to merge infos from soil moisture sensor and Et0 evaluation... for now we don't use it"""
#
# try:
#     soil_tension_list = db.getSoilSensorData()
#     #print(soil_tension_list)
#
#
#     mean = 0
#     std = 0
#     for result in soil_tension_list:
#         mean += float(result[0])
#     mean = mean/len(soil_tension_list)
#
#     for result in soil_tension_list:
#         std += (float(result[0]) - mean)**2
#     std = (std/len(soil_tension_list))**0.5
#
#     a_etc = 0.8 #weight for Etc in the final water quantity estimation
#     b_sensor = 1 - a_etc #weight for the soil tension sensor data
    #soil_tension_avg = mean
    #soil_tension_std = std
    # print(soil_tension_avg)
    # print(soil_tension_std)
    #soil_tension = float(soil_tension_list[0][0])
    # high soil_tension, means that the ground is dry

    # Since we don't know what are the  typical value for soil_tension,
    # maybe a good choice could be to compare the current value
    # with the mean value and the std

    # Normalize then....
    #soil_tension_norm  = (soil_tension - soil_tension_avg)/soil_tension_std

    # print(soil_tension_norm) # <--------- print that to understand i

    #water_quantity = a_etc * Etc + b_sensor * Etc * soil_tension_norm

    # print('Estimated water quantity is = ', water_quantity)
    #
    # #now let's export the data in a json format
#
# except:
#     print("cannot retrieve soil water tension from database")

try:

    json_dict = {"crop id": crop_id,
                 "ETc" : Etc,
                 "crop type " : crop_type,
                 "last update " : current_date.isoformat()
                 }

    with open('Greenhouse/Smart-Greenhouse/platform/ETc.json', 'w') as file:
        json.dump(json_dict, file)

except:
    print("cannot save the json file with trigger informations")


