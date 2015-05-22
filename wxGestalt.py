# -*- coding: utf-8 -*-

# Modules
# Modules for the wx GUI
import wx
import GUI.wxMainApp as wxMainApp
import GUI.wxTab as wxTab
# Various functions
import Functions.wxFunctions as wxFunctions
# Module for log
import sys


# Variables
# Current global setting for the Serial port in use
SerialPortInUse = ""


# Classes
# Class for redirecting the terminal to the log screen
class RedirectText(object):
    # Redirect the print message to the Status log area
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


# The class for the main app
class wxGestaltApp(wxMainApp.MyFrame1):

    def __init__(self, *args, **kw):
        super(wxGestaltApp, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.On_CreateTab(tabsNumber = 1,tabTitle = ["Welcome"])
        self.Show()

        # Starting the log
        # Redirect text here
        redir=RedirectText(self.wxLog)
        sys.stdout=redir

    def On_Quit( self, event ):
        self.Close(True)

    def On_ScanSerialPort( self, event ):
        # looks for available serial ports
        SerialPortsAvailable = wxFunctions.ScanSerialPorts()
        global SerialPortInUse
        # Global variable that can be accessed by the whole program
        dlg = wx.SingleChoiceDialog(self, 'Choose the serial port for your machine: ', 'Serial port settings', SerialPortsAvailable, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            SerialPortInUse = dlg.GetStringSelection()
            print "Connecting to",SerialPortInUse
        dlg.Destroy()

    def On_CreateTab(self, tabsNumber = 1, tabTitle =[]):
        # Create tabs in the notebook
        self.tabs = []
        for each_tab in range(tabsNumber):
            self.tabs.append(wxTab.MyPanel1(self.m_notebook1))
            self.m_notebook1.AddPage(self.tabs[each_tab], tabTitle[each_tab], False )

    def On_Message(self, title, content):
        # Open up a dialog
        dlg = wx.MessageDialog(self, content, title, wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':
    ex = wx.App()
    ex1 = wxGestaltApp(None)
    ex1.Show()
    ex.MainLoop()
