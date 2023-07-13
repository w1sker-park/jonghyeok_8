#!/usr/bin/env python

import json

STATUS_OK = 1
STATUS_ERR = 0

class Json_Data_List:
	content = []
	count = 0
	error = 0
	def save_json_data(self,json_data):
		Json_Data_List.count += 1
		Json_Data_List.content.append(json_data)
		print(len(Json_Data_List.content))
		if len(Json_Data_List.content) == Json_Data_List.count:
			return STATUS_OK
		else:
			Json_Data_List.count -= 1
			return STATUS_ERR

	def send_server():
		if not Json_Data_List.content:
			print(Json_Data_List.error)
			Json_Data_List.error += 1
			print("empty")
		elif Json_Data_List.content:
			print(Json_Data_List.content[-1])
			Json_Data_List.content.clear()
			Json_Data_List.count = 0

def test():
	json_dic = {"time_stamp": 123456,
			"data":
			{
			"road_temp": 12.3,
			"freezing_temp": 0.0,
                	"water_height": 0.0,
                	"thickness": 0.0,
                	"snow_height": 0.0,
                	"ice_percent": 0.0,
                	"saline_concent": 0.1,
                	"friction": 0.82,
                	"road_condition": 0,
                	"road_index": 0
                	}
            	}

	json_data = json.dumps(json_dic, indent = 2)

	json_data_list = Json_Data_List()
#	json_data_list.save_json_data(json_data)


for  i in range(2):
	test()

Json_Data_List.send_server()
print(len(Json_Data_List.content))
