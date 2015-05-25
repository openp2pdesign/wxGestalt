# -*- coding: utf-8 -*-

# Modules
# Modules for the wx GUI
import wx
import GUI.wxMainApp as wxMainApp
import GUI.wxTabSetup as wxTabSetup
import GUI.wxNodeTab as wxNodeTab
# Various functions
import Functions.wxFunctions as wxFunctions
# Module for log
import sys
# Module for Gestalt Machines
import Machines.wxMachines as wxMachines


# Variables
# Current global setting for the Serial port in use
SerialPortInUse = ""
# The current machine edited in the app
currentMachine = wxMachines.wxMachine()


# Classes
# Class for redirecting the terminal to the log screen
class RedirectText(object):
    # Redirect the print message to the Status log area
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


# The class for a tab
class wxTabSetup(wxTabSetup.MyPanel1):

    def On_OrganizeNodes( self, event ):
        # Add or remove nodes and therefore their GUI editing part
        if self.m_spinCtrl1.GetValue() < currentMachine.nodesNumber:
            self.m_notebook_nodes.DeletePage(self.m_spinCtrl1.GetValue())
        else:
            nodePage = wxNodeTab.MyPanel1(self.m_notebook_nodes)
            self.m_notebook_nodes.AddPage(nodePage,u"Node #"+str(currentMachine.nodesNumber+1))
            #self.ln = wx.StaticLine(self, -1, size=(400,10))
            #self.newButton = wx.StaticText(self, wx.ID_ANY, u"Node #"+str(currentMachine.nodesNumber))
            #self.ln.SetSize((30,30))
            #self.tabs[0].Add(self.ln, 0, wx.ALL, 5)
            #self.tabs[0].Add(self.newButton, 0, wx.ALL, 5)
            #self.tabs[0].Layout()
            #self.bSizer2.Layout()
        # Update the current Machine and the log
        currentMachine.nodesNumber = self.m_spinCtrl1.GetValue()
        if currentMachine.nodesNumber == 1:
            print "The Machine now has", currentMachine.nodesNumber, "Gestalt node."
        else:
            print "The Machine now has", currentMachine.nodesNumber, "Gestalt nodes."


# The class for the main app
class wxGestaltApp(wxMainApp.MyFrame1):

    def __init__(self, *args, **kw):
        super(wxGestaltApp, self).__init__(*args, **kw)
        global currentMachine
        self.InitUI()

    def InitUI(self):
        tab_setup = wxTabSetup(self.m_notebook1)
        self.m_notebook1.AddPage(tab_setup, "Machine Setup", False )
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
