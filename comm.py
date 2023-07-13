#!/usr/bin/env python

import serial
import crc16

SOH = 0x01
VER = 0x10
TO_1ST = 0x01
TO_2ND = 0x50
FROM_1ST = 0x01
FROM_2ND = 0xF0
LEN = 0x17
STX = 0x02
CMD = 0x2F
VERC = 0x10
P_NUM = 0x0A
P_ROAD_TEMP_1ST = 0x64
P_ROAD_TEMP_2ND = 0x00
P_FREZ_TEMP_1ST = 0x6E
P_FREZ_TEMP_2ND = 0x00
P_WATER_HEIGHT_1ST = 0x58
P_WATER_HEIGHT_2ND = 0x02
P_THICKNESS_1ST = 0x59
P_THICKNESS_2ND = 0x02
P_SNOW_HEIGHT_1ST = 0x62
P_SNOW_HEIGHT_2ND = 0x02
P_ICE_PERCENT_1ST = 0x20
P_ICE_PERCENT_2ND = 0x03
P_SALINE_CONCENT_1ST = 0x2A
P_SALINE_CONCENT_2ND = 0x03
P_FRICTION_1ST = 0x34
P_FRICTION_2ND = 0x03
P_ROAD_CONDITION_1ST = 0x84
P_ROAD_CONDITION_2ND = 0x03
P_ROAD_INDEX_1ST = 0x8E
P_ROAD_INDEX_2ND = 0x03
ETX = 0x03
EOT = 0x04
NO_ERROR = 0x00

DATA_READ_TIMEOUT = 3
SERIAL_READ_TIMEOUT = 1.0
SERIAL_WRITE_TIMEOUT = 1.0
READ_BYTES = 100

data = [
        SOH,
        VER,
        TO_1ST,
        TO_2ND,
        FROM_1ST,
        FROM_2ND,
        LEN,
        STX,
        CMD,
        VERC,
        P_NUM,
        P_ROAD_TEMP_1ST,
        P_ROAD_TEMP_2ND,
        P_FREZ_TEMP_1ST,
        P_FREZ_TEMP_2ND,
        P_WATER_HEIGHT_1ST,
        P_WATER_HEIGHT_2ND,
        P_THICKNESS_1ST,
        P_THICKNESS_2ND,
        P_SNOW_HEIGHT_1ST,
        P_SNOW_HEIGHT_2ND,
        P_ICE_PERCENT_1ST,
        P_ICE_PERCENT_2ND,
        P_SALINE_CONCENT_1ST,
        P_SALINE_CONCENT_2ND,
        P_FRICTION_1ST,
        P_FRICTION_2ND,
        P_ROAD_CONDITION_1ST,
        P_ROAD_CONDITION_2ND,
        P_ROAD_INDEX_1ST,
        P_ROAD_INDEX_2ND,
        ETX
        ]


def set_request_data():
	input_crc = format(crc16.crc16_mcrf4xx(data),'02x')
	input_cs_list = [int(input_crc[2:4],16), int(input_crc[0:2],16)]
	data.extend(input_cs_list)
	data.append(EOT)

	return data


def create_serial(port_name):
	ser = serial.Serial(port=port_name,
			baudrate=19200,
                        bytesize=8,
                        parity='N',
                        stopbits=1,
                        timeout=SERIAL_READ_TIMEOUT,
                        write_timeout=SERIAL_WRITE_TIMEOUT,
                        xonxoff=False,
                        rtscts=True,
                        dsrdtr=True
                        )
	return ser

