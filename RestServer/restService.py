import json
import cherrypy
import restOperations
import logging
import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))


class RestServer(restOperations.RestOperations):
	exposed = True

	def __init__(self):
		restOperations.RestOperations.__init__(self)
		logging.basicConfig(format='%(asctime)s - %(message)s',filename="logfilename.log", level=logging.INFO)
		self.dataFile = os.path.join(cur_path,'../platform/irrigation.json')
		self.manualTrigger = False
		self.automaticTrigger = False
		self.cropId = 0

	def OPTIONS(self, *uri, **params):
		cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])

	def GET(self, *uri, **params):
		try:
			if len(uri) != 0 :
				cmd = uri[0]
				if(cmd == "getDataPS"):
					result = self.getDataForPS(self.manualTrigger,self.cropId)
					self.manualTrigger = False
					self.automaticTrigger = False
					return result

				elif(cmd == "getAllCrops"):
					return self.getAllCrops()
				
				elif(cmd == "getAllCropsForUI"):
					return self.getAllCropsForUI()

				elif(cmd == "manualTriggerOn"):
					self.manualTrigger = True
					if params != {}:
						self.cropId = params['cropId']
					return "true"

				elif(cmd == "getCropData"):
					if params != {}:
						cropId = params['cropId']
						return self.getCropData(cropId)

		except Exception as ex:
			logging.info(ex)
			raise Exception
			
	def POST(self, *uri, **params):
		try:
			if len(uri) != 0 :
				cmd = uri[0]
				rawData = cherrypy.request.body.read()
				data = json.loads(rawData)

				if(cmd == "login"):
					userData = data
					print(userData)
					return self.login(userData)

				elif(cmd == "editCrop"):
					cropData = data
					if params != {}:
						cropId = params['cropId']
						return self.editCrop(cropId, cropData)
		except Exception as ex:
			logging.info(ex)
			raise Exception

if __name__ == "__main__":

	conf = {
		'/' : {
				'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
            	# required for CORS
            	"tools.response_headers.on": True,
            	"tools.response_headers.headers": [
                ("Access-Control-Allow-Origin", "*"),
                ],      
				'tool.session.on' : True
		}
	}



	app = cherrypy.tree.mount(RestServer(),'/',conf)
	cherrypy.config.update({'server.socket_host':'0.0.0.0'})
	cherrypy.config.update({'server.socket_port': 1628})
	cherrypy.engine.start()
	cherrypy.engine.block()