#!/usr/bin/env python

import json
import jsonpickle
import comm
import struct
import datetime

STATUS_OK = 1
STATUS_ERR = 0

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

class Status_Error:
	def __str__(self):
		return "Status_Error"


def time_stamp():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d T %H:%M:%S +09:00')
	return timestamp


def lufft_protocol_check(rcv_data):
	if rcv_data[0:6] == bytes([comm.SOH, comm.VER, comm.FROM_1ST, comm.FROM_2ND, comm.TO_1ST, comm.TO_2ND]) and rcv_data[len(rcv_data)-1] == 4:
		return STATUS_OK
	else:
		return STATUS_ERR


def lufft_protocol_decode(rcv_data):
	lufft_dto = Lufft_DTO()

	road_temp = ''
	freezing_temp = ''
	water_height = ''
	thickness = ''
	snow_height = ''
	ice_percent = ''
	saline_concent = ''
	friction = ''
	road_condition = ''
	road_index = ''
	status = STATUS_ERR

	try:
		if rcv_data[10] != comm.NO_ERROR:
			raise Status_Error()

		for j in range(20, 16, -1):
			road_temp += format(rcv_data[j],'02x')
		road_temp = round(struct.unpack('!f', bytes.fromhex(road_temp))[0],4)

		for j in range(29, 25, -1):
			freezing_temp += format(rcv_data[j],'02x')
		freezing_temp = round(struct.unpack('!f', bytes.fromhex(freezing_temp))[0],4)

		for j in range(38, 34, -1):
			water_height += format(rcv_data[j],'02x')
		water_height = round(struct.unpack('!f', bytes.fromhex(water_height))[0],4)

		for j in range(47, 43, -1):
			thickness += format(rcv_data[j],'02x')
		thickness = round(struct.unpack('!f', bytes.fromhex(thickness))[0],4)

		for j in range(56, 52, -1):
			snow_height += format(rcv_data[j],'02x')
		snow_height = round(struct.unpack('!f', bytes.fromhex(snow_height))[0],4)

		for j in range(65, 61, -1):
			ice_percent += format(rcv_data[j],'02x')
		ice_percent = round(struct.unpack('!f',bytes.fromhex(ice_percent))[0],4)

		for j in range(74, 70, -1):
			saline_concent += format(rcv_data[j],'02x')
		saline_concent = round(struct.unpack('!f', bytes.fromhex(saline_concent))[0],4)

		for j in range(83, 79, -1):
			friction += format(rcv_data[j],'02x')
		friction = round(struct.unpack('!f', bytes.fromhex(friction))[0],4)

		road_condition = rcv_data[89]

		road_index = rcv_data[95]

		status = STATUS_OK

		lufft_dto.data.road_temp = road_temp
		lufft_dto.data.freezing_temp = freezing_temp
		lufft_dto.data.water_height = water_height
		lufft_dto.data.thickness = thickness
		lufft_dto.data.snow_height = snow_height
		lufft_dto.data.ice_percent = ice_percent
		lufft_dto.data.saline_concent = saline_concent
		lufft_dto.data.friction = friction
		lufft_dto.data.road_condition = road_condition
		lufft_dto.data.road_index = road_index
		lufft_dto.timestamp = time_stamp()

		json_data = jsonpickle.encode(lufft_dto, unpicklable = False)


	except Ststus_Error as e:
		print(e)
	except:
		print(e)

	return json_data, status

