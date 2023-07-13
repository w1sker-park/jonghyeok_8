#!/usr/bin/env python

import threading
import time

STATUS_OK = 1
STATUS_ERR = 0

time_interval = 10
json_data_list = []


class list:
	count = 0

class error:
	count = 0


def save_json_data(json_data):
    list.count += 1
    json_data_list.append(json_data)
    if len(json_data_list) == list.count:
        return STATUS_OK
    else:
        list.count -= 1
        return STATUS_ERR


def send_server():
	if not json_data_list:
		print(error.count)
		error.count += 1
		print("empty")

	elif json_data_list:
		print(json_data_list[-1])
		json_data_list.clear()
		list.count = 0


	threading.Timer(time_interval, send_server).start()

                # TODO Exception handling

