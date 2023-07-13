#!/usr/bin/env python

import comm

STATUS_OK = 1
STATUS_ERR = 0


def crc16_mcrf4xx(data):
    crc = 0xFFFF
    for i in range(len(data)):
        byte = data[i]
        for b in range(8):
            crc ^= (byte & 0x01)
            crc = ((crc >> 1) ^ 0x8408) if (crc & 0x01) else (crc >> 1)
            byte >>= 1

    return crc


def crc_check(rcv_data):
    output_crc = format(crc16_mcrf4xx(rcv_data[:comm.READ_BYTES - 3]), '02x')
    output_crc_list = [int(output_crc[2:4], 16), int(output_crc[0:2], 16)]

    if output_crc_list == [rcv_data[comm.READ_BYTES - 3], rcv_data[comm.READ_BYTES - 2]]:
        return STATUS_OK
    else:
        return STATUS_ERR

