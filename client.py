import json
import requests
import threading
import datetime
import jsonpickle

time_interval = 10

def time_stamp():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d T %H:%M:%S +09:00')
	return timestamp



class Lufft_DTO:
	def __init__(self):
		self.data = self.Data()
		self.time_stamp : str

	class Data:
		def __init__(self):
			self.road_temp : float
			self.freezing_temp : float
			self.water_height : float
			self.thickness : float
			self.snow_height : float
			self.ice_percent : float
			self.saline_concent : float
			self.friction : float
			self.road_condition : int
			self.road_index : int

lufft_dto = Lufft_DTO()

lufft_dto.data.road_temp = 25.6
lufft_dto.data.freezing_temp = 0.0
lufft_dto.data.water_height = 0.0
lufft_dto.data.thickness = 0.0
lufft_dto.data.snow_height = 0.0
lufft_dto.data.ice_percent = 0.0
lufft_dto.data.saline_concent = 0.0
lufft_dto.data.friction  = 0.82
lufft_dto.data.road_condition = 0
lufft_dto.data.road_index = 0
lufft_dto.timestamp = time_stamp()

json_data = jsonpickle.encode(lufft_dto, unpicklable = False, indent = 2)
print(json_data)


def send():

	res = requests.post('http://localhost:5000/test', json = json_data)
	print(res.content)
	print(datetime.datetime.now())
	threading.Timer(time_interval, send).start()

send()
