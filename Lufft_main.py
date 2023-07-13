#!/usr/bin/env python

import comm
import crc16
import data_handle
import send_server
import time
import datetime
import threading
import os


class Json_Data:
	list = []
	count = 0
	def save_json_data(self, json_data):
		self.count += 1
		self.list.append(json_data)
		if len(self.list) == self.count:
			return STATUS_OK
		else:
			self.count -= 1
			return STATUS_ERR


class Write_Error(Exception):
	def __str__(self):
		return "Write_Error"

class Read_Error(Exception):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return "Read_Error res = %d"  %self.value

class Lufft_Protocol_Error(Exception):
	def __str__(self):
		return "Lufft_Protocol_Error"

class Check_Sum_Error(Exception):
	def __str__(self):
		return "Check_Sum_Error"

def init():
	os.system("sudo sh -c 'echo out > /sys/class/gpio/gpio18/direction'")

def initialization():
#	os.system("sudo sh -c 'echo 18 /sys/class/gpio/unexport'")
	os.system("sudo sh -c 'echo 18 /sys/class/gpio/export'")

	ser = comm.create_serial("/dev/ttyS0")

	if ser.is_open:
		ser.close()
	ser.open()

	data_req = comm.set_request_data()

	send_server.send_server()

	return ser, data_req


def serial_flush():
	ser.flushInput()
	ser.flushOutput()

def check_timeout(last_time):
	time_dif = time.time() - last_time
	if time_dif >= comm.SERIAL_READ_TIMEOUT:
		serial_flush()
		flag = True
		timeout += time_dif
		if timeout >= comm.DATA_READ_TIMEOUT:
			timeout = 0
			reconnect()
			print("Read_Timeout")
			print(datetime.datetime.now())
			return
		break

def request():
	global timeout
	global flag
	flag = True
	timeout = 0
	decode_status = data_handle.STATUS_ERR
#	res = b''
	save_cnt = 0
	json_data = str()

	past_time = time.time()

	while flag:
		init()
		last_time = time.time()
		serial_flush()
		os.system("sudo sh -c 'echo 1 > /sys/class/gpio/gpio18/value'")
		time.sleep(0.01)
		try:
			write_size = ser.write(data_req)

			if write_size != len(data_req):
				raise Write_Error()

			time.sleep(0.01)
			os.system("sudo sh -c 'echo 0 > /sys/class/gpio/gpio18/value'")
			while 1:
				res = ser.read(comm.READ_BYTES)

				if len(res) != comm.READ_BYTES:
					raise Read_Error(res)

				if not data_handle.lufft_protocol_check(res):
					raise Lufft_Protocol_Error()

				if not crc16.crc_check(res):
					raise Check_Sum_Error()

				flag = False
				break

		except Write_Error as e:
			print(e)
			check_timeout(last_time)
		except Read_Error as e:
			print(e)
			check_timeout(last_time)
		except Lufft_Protocol_Error as e:
			print(e)
			check_timeout(last_time)
		except Check_Sum_Error as e:
			print(e)
			check_timeout(last_time)

	if not flag:
		json_data, decode_status = data_handle.lufft_protocol_decode(res)

	if decode_status:
		while save_cnt <= 2:
			if send_server.save_json_data(json_data):
				break
			save_cnt += 1
		if save_cnt == 3:
			print("save_error")
		print("now - start = %.3f" % (time.time() - past_time))
		time.sleep(comm.DATA_READ_TIMEOUT - (time.time() - past_time))
	else:
		serial_flush()


def reconnect():
	os.system("sudo sh -c 'echo 18 > /sys/class/gpio/unexport'")
	os.system("sudo sh -c 'echo 18 > /sys/class/gpio/export'")

	if ser.is_open:
		ser.close()
	ser.open()
	print("reconnect")


# --main--
ser, data_req = initialization()

while 1:
	try:
		request()

	except:
		ser.close()
		break

    # TODO: Exception Handling

#ser, data_req = initialization()

thread1 = threading.Thread(target=send_server.send_server)

thread1.start()

