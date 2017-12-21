#!/usr/bin/env python                                                                                                                           

import json
from flask import Flask, request
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app) # api is a collection of objects, where each object contains a specific functionality (GET, POST, etc)

#headers for requests to GM API
headers = {

    'Content-Type': 'application/json',

}

#Api error exception class
class ApiError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

#Object to interface with GM api getVehicleInfoService
class Vehicle_Info(Resource):
	def get(self,vehicle_id):
		data = '{"id": "'+vehicle_id+'", "responseType": "JSON"}'
		#post request to GM API and get response
		response = requests.post('http://gmapi.azurewebsites.net/getVehicleInfoService', headers=headers, data=data)
		if response.status_code != 200:
    			# This means something went wrong.
			raise ApiError('GET /vehicles/{} {}'.format(vehicle_id,response.status_code))
		output_dict = {}
		#Iterate through request response
		for info,value in response.json()['data'].items():
			if value['type'] == 'String':
				output_dict[info] = value['value']
			elif value['type'] == 'Boolean' and value['value'] == 'True':
				if 'twoDoor' in info:
					output_dict['doorCount'] = 2
				else:
					output_dict['doorCount'] = 4
		return json.dumps(output_dict)


#object to interface with GM API getSecurityStatusService
class Security_Status(Resource):
	def get(self,vehicle_id):
		data = '{"id": "'+vehicle_id+'", "responseType": "JSON"}'
		#post request to GM API and get response
		response = requests.post('http://gmapi.azurewebsites.net/getSecurityStatusService', headers=headers, data = data)

		if response.status_code != 200:
			raise ApiError('GET /vehicles/{}/doors {}'.format(vehicle_id,response.status_code))
		output_array = []
		#Iterate through request response
		for info,value in response.json()['data'].items():
			if value['type'] == 'Array':                                                                                         
				for doorInfo in value['values']:
					door_dict = {}
					for dInfo,dValue in doorInfo.items():
						if dValue['type'] == 'String':
							door_dict[dInfo]=dValue['value']
						elif dValue['type'] == 'Boolean':
							door_dict[dInfo]=dValue['value']
					output_array.append(door_dict)
		return json.dumps(output_array)

#object to interface with GM API getEnergyService
class Energy_Level(Resource):
	def get(self,vehicle_id,energy_type):
		data = '{"id": "'+vehicle_id+'", "responseType": "JSON"}'
		#post request to GM API and get response
		response = requests.post('http://gmapi.azurewebsites.net/getEnergyService', headers=headers, data = data)
		if response.status_code != 200:
			raise ApiError('GET /vehicles/{}/{} {}'.format(vehicle_id,energy_type,response.status_code))
		output_dict = {}
		#check if request is to get fuel level
		if energy_type == 'fuel':
			if response.json()['data']['tankLevel']['type'] == 'Number':
				output_dict['percent'] = response.json()['data']['tankLevel']['value']
			else:
				output_dict['percent'] = 'N/A; No fuel tank'
		#check if request is to get battery level
		elif energy_type == 'battery':
			if response.json()['data']['batteryLevel']['type'] == 'Number':
				output_dict['percent'] = response.json()['data']['batteryLevel']['value']
			else:
				output_dict['percent'] = 'N/A; No battery'
		return json.dumps(output_dict)

#object to interface with GM API actionEngineService
class Engine_Action(Resource):
	def post(self,vehicle_id):
		content = request.get_json()
		data = '{"id": "'+vehicle_id+'","command": "'+content['action']+'_VEHICLE", "responseType": "JSON"}'
		#post request to GM API and get response
		response = requests.post('http://gmapi.azurewebsites.net/actionEngineService', headers=headers, data = data)
		if response.status_code != 200:
			raise ApiError('POST /vehicles/{}/engine {}'.format(vehicle_id,response.status_code))

		output_dict = {}
		#check if action has been executed
		if response.json()['actionResult']['status'] == 'EXECUTED':
			output_dict['status'] = 'success'
		else:
			output_dict['status'] = 'error'

		return json.dumps(output_dict)

api.add_resource(Vehicle_Info, '/vehicles/<string:vehicle_id>',methods = ['GET'])  # bind url identifier to class; also make it querable
api.add_resource(Security_Status, '/vehicles/<string:vehicle_id>/doors',methods = ['GET'])
api.add_resource(Energy_Level, '/vehicles/<string:vehicle_id>/<string:energy_type>',methods = ['GET'])
api.add_resource(Engine_Action, '/vehicles/<string:vehicle_id>/engine', methods = ['POST'])


if __name__ == '__main__':

    app.run(debug=True)
				

