import json
from datetime import datetime, timedelta


#first part of the code can be used as base for irrigation every more days and not daily (or for more irrigations during the same day)

'''#TODO: use a daily loop to avoid interruption

##### RUN ONLY ONCE #####
CHECK_INTERVAL = 30 #in minutes ---> time interval between every readings of soil moisture sensor
db = dbconnection.db_connection()
LOOP = True
THRESHOLD = 5000    #TODO: discuss with prof zavattaro
WATER_FLOW = 0.05 #TODO: to be find
N_OF_IRRIGATIONS_PER_DAY = 1


#first of all read the ETC value

path_json_file = 'Greenhouse/Smart-Greenhouse/platform/ETc.json'
file = open(path_json_file)
data = json.load(file)

ETc = data['ETc'] #that's the ammount of water we need to give to the plant
opening_time = int(ETc/WATER_FLOW)

"""now we need to decide when start the irrigation. The idea is to use the soil moisture tension sensor since we can
assume that the irrigation is totally controlled, we have the evapotranspiration and we also knows that rain will be 0 (closed environment)"""

while LOOP:

#check now the values of the sensor
    try:
        soil_tension_list = db.getSoilSensorData()
        soil_tension_value = float(soil_tension_list[0][0])

    except:
        print('cannot retrieve data from db')

    if soil_tension_value >= THRESHOLD:

        "starting time and write a json file"
        now =  datetime.now()

        start = now + timedelta(minutes=30) #start irrigation 30 minutes after we reached the threshold (field capacity)

        end = start + timedelta(seconds=opening_time) #keep the valve opened for the 'opening_time'
        start = start.strftime("%d/%m/%Y %H:%M:%S")
        end = end.strftime("%d/%m/%Y %H:%M:%S")
        json_dict = {"start irrigation": start,
                     "stop irrigation": end
                     }

        with open('Greenhouse/Smart-Greenhouse/platform/irrigation.json', 'w') as file:
            json.dump(json_dict, file)

        LOOP = False


    else:
        time.sleep(CHECK_INTERVAL * 60)

'''

def trigger():
    WATER_FLOW = 0.005  # TODO: to be find
    POT_SURFACE = 0.2 #m**2 ---> pot surface #TODO: to be find
    #first of all read the ETC value

    path_json_file = 'Greenhouse/Smart-Greenhouse/platform/ETc.json'
    file = open(path_json_file)
    data = json.load(file)

    ETc = data['ETc']
    crop_id = data['crop id']
    needed_water = ETc * POT_SURFACE #that's the ammount of water we need to give to the plant
    opening_time = int(needed_water/WATER_FLOW) #in seconds

    now = datetime.now()

    start = datetime(now.year, now.month, now.day, 6, 0, 0) #start irrigation at 6 am UTC
    end = start + timedelta(seconds=opening_time)  # keep the valve opened for the 'opening_time'

    start = start.strftime("%d/%m/%Y %H:%M:%S")

    end = end.strftime("%d/%m/%Y %H:%M:%S")
    json_dict = {"crop id": crop_id, "start irrigation": start, "stop irrigation": end, "last_update": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

    with open('Greenhouse/Smart-Greenhouse/platform/irrigation.json', 'w') as file:
        json.dump(json_dict, file)

