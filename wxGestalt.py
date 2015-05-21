# -*- coding: utf-8 -*-

# Modules
# Modules for the wx GUI
import wx
import GUI.wxClass as wxClass
# Modules for the serial communication
import serial
from serial.tools import list_ports


# Variables
# Current global setting for the Serial port in use
SerialPortInUse = ""


# Functions
def ScanSerialPorts():
    # Scan for available ports. return a list
    ListedPorts = []
    for i in list_ports.comports():
        ListedPorts.append(i[0])
    return ListedPorts


# Classes
# The class for the main app
class wxGestaltApp(wxClass.MyFrame1):

    def __init__(self, *args, **kw):
        super(wxGestaltApp, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.Show()

    def On_Quit( self, event ):
        self.Close(True)

    def On_ScanSerialPort( self, event ):
        # looks for available serial ports
        SerialPortsAvailable = ScanSerialPorts()
        global SerialPortInUse
        # Global variable that can be accessed by the whole program
        dlg = wx.SingleChoiceDialog(self, 'Choose the serial port for your machine: ', 'Serial port settings', SerialPortsAvailable, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            SerialPortInUse = dlg.GetStringSelection()
            print SerialPortInUse
        dlg.Destroy()


if __name__ == '__main__':
    ex = wx.App()
    ex1 = wxGestaltApp(None)
    ex1.Show()
    ex.MainLoop()
