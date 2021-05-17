import dbconnection
import db_connect
import ast

db = dbconnection.db_connection()
# Et0 = db.getET0
Et0 = 4
#at this point we need to evaluate etc.

#TODO: in this way, kc it is constant but actually it depend on the crop
# constants needed for evaluation of Kc. Those depend on the crop type and we store them in a dict
kcb = {}
kcb['ini'] = 0.15
kcb['mid'] = 1.2 #---> originary it was 0.95 but on page 124 it is stated that for frequent irrigation is better to put it at 1.2
kcb['end'] = 0.85
RHmin = ast.literal_eval(db.getDataForParameter())['min_hum']



# TODO maybe let's find how many time the basil require to grow up from the seeds and then consider a linear growht (also if it is not true it should not be a big deal)
h = {}
h['ini'] = 0.2
h['mid'] = 0.4
h['end'] = 0.4

period = 'mid' #TODO find a way to evaluate the period { ini,mid,end} to decide k accordingly
correction_factor = -0.08 - 0.004 * (RHmin - 45) * (h[period] / 3) ** 0.3

#now we need to calibrate them in base of our actual enviromental conditions
if period == 'ini':
    Kcb = kcb[period]

else:
    Kcb = kcb[period] + correction_factor

#print('Kcb = ',Kcb)

#now let's think to Ke

kr = 0.9 #set equal to 0.9 for sake of semplicity, if you have time modify it accordingly with page 145 (really time expensive)
Kcmax = min(1.2+correction_factor, Kcb + 0.5)

#print('Kcmax = ', Kcmax)

Ke = kr * (Kcmax - Kcb)

#print("Ke = ", Ke)

Kc = Ke + Kcb

Etc = Et0 * Kc

print( "with the current Kc =", Kc, 'the resulting Etc = ', Etc)


soil_tension = float(db.getDataLastEpoch()[-2][1] ) #getting soil tension from the database

mydb = db_connect.connect()
mycursor = mydb.cursor()
considered_days = 15
considered_samples = considered_days * 24 * 4
select = "SELECT value FROM sensorParser WHERE sensor = 'SOIL3' ORDER BY timestamp DESC LIMIT "+str(considered_samples)
mycursor.execute(select)
myresult = mycursor.fetchall()

mean = 0
std = 0
for result in myresult:
    mean += float(result[0])
mean = mean/considered_samples

for result in myresult:
    std += (float(result[0]) - mean)**2
std = (std/considered_samples)**0.5

a_etc = 0.8 #weight for Etc in the final water quantity estimation
b_sensor = 1 - a_etc #weight for the soil tension sensor data
soil_tension_avg = mean
soil_tension_std = std
# high soil_tension, means that the ground is dry

# Since we don't know what are the  typical value for soil_tension,
# maybe a good choice could be to compare the current value
# with the mean value and the std

# Normalize then....

water_quantity = a_etc * Etc + b_sensor * (Etc*(soil_tension - soil_tension_avg)/soil_tension_std)

print(' water quantity estimated is = ', water_quantity)




