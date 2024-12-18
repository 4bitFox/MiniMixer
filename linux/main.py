#!/usr/bin/env python3

import MiniMixer as MM

MM.serial.init("3273e2cefa50a16eafefca053ba87625")
while True:
    serial = MM.serial.serial_data
    if serial != None:
        #print(serial)
        serial_dict = MM.evaluate.serial2dict(serial)
        print(serial_dict)
