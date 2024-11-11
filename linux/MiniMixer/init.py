#!/usr/bin/env python3
import os
import threading
from time import sleep



serial_data = None
dev_identifier = None


def _device_identity_check(dev_data):
    if dev_data.startswith("Device: " + dev_identifier + ";"):
        return True
    else:
        return False


def _device_find():
    dev_dir = "/dev"

    print("Trying to find device...")
    while True:
        dev_ls = os.listdir(dev_dir) # ls /dev
        for dev_file in dev_ls:
            if "ttyACM" in dev_file:
                dev_path = dev_dir + "/" + dev_file
                dev_data = _device_read(dev_path, continuous = False)
                if _device_identity_check(dev_data):
                    print("Device found!")
                    return dev_path
        sleep(1)


def _device_read(device = "/dev/ttyACM0", continuous = False):
    #print("Trying to access device " + device + "    continuous: " + str(continuous))
    try:
        with open(device, 'r') as serial_port:
            while True:
                data = serial_port.readline()  # read one line from the device
                if not continuous:
                    serial_port.close()
                    return data

                global serial_data
                serial_data = data

                if not _device_identity_check(data):
                    print("Connection to device lost!")
                    serial_port.close()
                    serial_data = None
                    init(dev_identifier) # reinitialize
                    break #prevent this thread from continuing to loop so it can exit and not interfere with new threads
    except FileNotFoundError as e:
        print("Device likely unplugged while opening. Reinitializing...    " + str(e))
        init(dev_identifier)  # reinitialize


def _device_read_thread(device):
    background_thread = threading.Thread(target=_device_read, kwargs={"device": device, "continuous": True})
    background_thread.daemon = True  # End daemon when main program exits
    background_thread.start()


def init(identifier):
    global dev_identifier
    dev_identifier = identifier

    device = _device_find()
    _device_read_thread(device)

    print("Initialized!")
