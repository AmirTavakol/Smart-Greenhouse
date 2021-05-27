import dbconnection
import db_connect
import ast
import json


db = dbconnection.db_connection()
try:
    Et0 = float(db.getET0Value()[0][0])
except:
    print("cannot retrieve Evapotranspiration from database")
#at this point we need to evaluate etc.

try:
    file = open('Greenhouse/Smart-Greenhouse/platform/basil.json')
    data = json.load(file)
    kcb = data['Kcb'] #constant for Etc. It depends on the crop type and age
    h = data[
        'height']  # TODO maybe let's find how many time the basil require to grow up from the seeds and then consider a linear growht (also if it is not true it should not be a big deal)

except:
    print("File not found")


#print(data['Kcb'])

period = 'mid' #TODO find a way to evaluate the period { ini,mid,end} to decide k accordingly


try:
    RHmin = ast.literal_eval(db.getDataForParameter())['min_hum']
    #corerction factor for Kcb
    correction_factor = -0.08 - 0.004 * (RHmin - 45) * (h[period] / 3) ** 0.3
except:
    print("cannot retrieve data from database, hence it is not possible to evaluate the correction factor for Kcb ")

try:
    #now we need to calibrate them in base of our actual environmental conditions
    if period == 'ini':
        Kcb = kcb[period]
        #here modify the height as well... if you are in the initial phase, the height is not constant, multiply it by a factor depending on the day

    else:
        Kcb = kcb[period] + correction_factor
except:
    print("cannot evaluate Kcb, check the database connection or the json file containing kcb factors ")

#print('Kcb = ',Kcb)

#now let's think to Ke
try:
    kr = 0.9 #set equal to 0.9 for sake of semplicity, if you have time modify it accordingly with page 145 (really time expensive)
    Kcmax = min(1.2+correction_factor, Kcb + 0.5)

    #print('Kcmax = ', Kcmax)

    Ke = kr * (Kcmax - Kcb)

    #print("Ke = ", Ke)

    Kc = Ke + Kcb

    Etc = Et0 * Kc
except:
    print("")
print( "with the current Kc = ", Kc, 'the resulting Etc is ', Etc)

try:
    soil_tension_list = db.getSoilSensorData()
    #print(soil_tension_list)


    mean = 0
    std = 0
    for result in soil_tension_list:
        mean += float(result[0])
    mean = mean/len(soil_tension_list)

    for result in soil_tension_list:
        std += (float(result[0]) - mean)**2
    std = (std/len(soil_tension_list))**0.5

    a_etc = 0.8 #weight for Etc in the final water quantity estimation
    b_sensor = 1 - a_etc #weight for the soil tension sensor data
    soil_tension_avg = mean
    soil_tension_std = std
    # print(soil_tension_avg)
    # print(soil_tension_std)
    soil_tension = float(soil_tension_list[0][0])
    # high soil_tension, means that the ground is dry

    # Since we don't know what are the  typical value for soil_tension,
    # maybe a good choice could be to compare the current value
    # with the mean value and the std

    # Normalize then....
    soil_tension_norm  = (soil_tension - soil_tension_avg)/soil_tension_std

    # print(soil_tension_norm) # <--------- print that to understand i

    water_quantity = a_etc * Etc + b_sensor * Etc * soil_tension_norm

    print('Estimated water quantity is = ', water_quantity)

    #now let's export the data in a json format

except:
    print("cannot retrieve soil water tension from database")

try:
    #TODO: decide when activate the irrigation system
    json_dict = {"water quantity": water_quantity,
                 "irrigation on" : "",
                 "irrigation off": ""
                 }

    with open('Greenhouse/Smart-Greenhouse/platform/trigger.json', 'w') as file:
        json.dump(json_dict, file)

except:
    print("cannot save the json file with trigger informations")


