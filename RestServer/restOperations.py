import json
from datetime import datetime
import sys
import os
from geopy.geocoders import Nominatim
from dateutil import tz
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import dbconnection 

class RestOperations(object):
	def __init__(self):
		self.conn = dbconnection.db_connection()
		self.geolocator = Nominatim(user_agent="geoapiExercises")

	def getAllCrops(self):
		result =[]
		result = self.conn.getAllCrops()
		return result
	
	def getAllCropsForUI(self):
		result = ""
		result = self.conn.getAllCrops()
		dictL = json.loads(result)
		dictR = []
		location = json.loads(self.conn.getClientLocation())[0]
		locationReverse = self.geolocator.reverse(str(location['latitude'])+","+str(location['longitude']))
		address = locationReverse.raw['address']
		town = address.get('town', '')
		county = address.get('county', '')
		cropLocation = town + ', ' + county
		for crop in dictL:
			t={}
			t['id'] = crop['id']
			t['cropName'] = crop['name']
			lastIrrigationData = self.conn.getLastIrrigationData(crop['id'])
			if lastIrrigationData != []:
				lastDataObj = lastIrrigationData[0][0]
				currentDate = datetime.utcnow()
				if (currentDate-lastDataObj).days >= 4:
					t['cropCondition'] = 'Critical'
				elif (currentDate-lastDataObj).days >= 2:
					t['cropCondition'] = 'Normal'
				elif (currentDate-lastDataObj).days < 2:
					t['cropCondition'] = 'Healthy'
				else:
					t['cropCondition'] = ''
			t['cropLocation'] = cropLocation
			t['imageUrl'] = '../assets/images/' + crop['name'] +'.jpg'
			dictR.append(t)
		print(dictR)	
		return json.dumps(dictR)		

	def login(self, userData):
		result = {}
		result = self.conn.login(userData)
		return result

	def editCrop(self, cropId, cropData):
		pass

	def getCropData(self, cropId):
		result = {}
		data = json.loads(self.conn.getCropData(cropId))
		location = json.loads(self.conn.getClientLocation())[0]
		locationReverse = self.geolocator.reverse(str(location['latitude'])+","+str(location['longitude']))
		address = locationReverse.raw['address']
		amenity = address.get('amenity', '')
		town = address.get('town', '')
		county = address.get('county', '')
		country = address.get('country', '')
		cropLocation = amenity + ', ' + town + ', ' + county
		lastIrrigationData = self.conn.getLastIrrigationData(cropId)
		if lastIrrigationData != []:
			lastDataObj = lastIrrigationData[0][0]
			currentDate = datetime.utcnow()
			if (currentDate-lastDataObj).days >= 4:
				result['cropCondition'] = 'Critical'
			elif (currentDate-lastDataObj).days >= 2:
				result['cropCondition'] = 'Normal'
			elif (currentDate-lastDataObj).days < 2:
				result['cropCondition'] = 'Healthy'
			else:
				result['cropCondition'] = ''

		result['id'] = data['id']
		result['cropName'] = data['name']
		result['dateSeeded'] = datetime.strptime(str(data['dateseeded']), '%Y-%m-%d %H:%M:%S.%f').strftime("%d %B, %Y")
		result['lastIrrigation'] = lastIrrigationData[0][0].replace(tzinfo=from_zone).astimezone(to_zone).strftime("%d %B, %Y, %H:%M")
		result['grafanaURL'] = data['grafanaUrl']
		result['cropLocation'] = cropLocation


		return json.dumps(result)

	def getDataForPS(self, manualTrigger, cropId = 0):
		result = {}
		autoMaticTrigger = False
		startDateTime = None
		endDateTime = None
		duration = 35
		with open(self.dataFile) as file:
			if file != '':
				data = json.load(file)
				
				if data:
					startDateTime = datetime.strptime(str(data['start irrigation']), '%d/%m/%Y %H:%M:%S')
					endDateTime = datetime.strptime(str(data['stop irrigation']), '%d/%m/%Y %H:%M:%S')
					duration = (endDateTime-startDateTime).total_seconds()
					cropId = data['crop id']
				
					lastData = self.conn.getLastIrrigationData(cropId)
					print(lastData)
					currentDate = datetime.utcnow()
					if lastData != []:
						lastDataObj = lastData[0][0]
						print(lastDataObj)
						if currentDate >= startDateTime and (currentDate-lastDataObj).days != 0:
							autoMaticTrigger = True
					else:
						if currentDate >= startDateTime:
							autoMaticTrigger = True

		if autoMaticTrigger or manualTrigger:
			result['trigger'] = True
			if self.manualTrigger:
				result['duration'] = 35
			else:
				result['duration'] = int(3*duration)
		else:
			result['trigger'] = False
			result['duration'] = 0

						
		if result['trigger'] == True:
			self.conn.saveIrrigationData(cropId,result['duration'],manualTrigger)

		return str(result['trigger']) + ',' + str(result['duration'])