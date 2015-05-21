# -*- coding: utf-8 -*-

# Import
# Modules for the serial communication
import serial
from serial.tools import list_ports


def ScanSerialPorts():
    # Scan for available ports. return a list
    ListedPorts = []
    for i in list_ports.comports():
        ListedPorts.append(i[0])
    return ListedPorts
