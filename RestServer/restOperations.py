import json
from datetime import datetime
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import dbconnection 

class RestOperations(object):
	def __init__(self):
		self.conn = dbconnection.db_connection() 

	def getAllCrops(self):
		result = ""
		result = self.conn.getAllCrops()
		return result		

	def getCropData(self, cropId):
		pass

	def login(self, userData):
		result = {}
		result = self.conn.login(userData)
		return result

	def editCrop(self, cropId, cropData):
		pass

	def getCropData(self, cropId):
		result = {}
		result = self.conn.getCropData(cropId)
		return result

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
					currentDate = datetime.utcnow()
					if lastData != []:
						lastDataObj = lastData[0][0]
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
				result['duration'] = 2*duration
		else:
			result['trigger'] = False
			result['duration'] = 0

						
		if result['trigger'] == True:
			self.conn.saveIrrigationData(cropId,duration)

		return json.dumps(result)