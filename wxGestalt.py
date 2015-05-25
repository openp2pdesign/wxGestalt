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


# The class for the Setup tab
class wxTabSetup(wxTabSetup.MyPanel1):

    def On_OrganizeNodes( self, event ):
        # Add or remove nodes and therefore their GUI editing part
        if self.m_spinCtrl1.GetValue() < currentMachine.nodesNumber:
            self.m_notebook_nodes.DeletePage(self.m_spinCtrl1.GetValue())
        else:
            nodePage = wxNodeTabSetup(self.m_notebook_nodes)
            self.m_notebook_nodes.AddPage(nodePage,u"Node #"+str(currentMachine.nodesNumber+1))

        # Update the current Machine and the log
        currentMachine.nodesNumber = self.m_spinCtrl1.GetValue()
        if currentMachine.nodesNumber == 1:
            print "The Machine now has", currentMachine.nodesNumber, "Gestalt node."
        else:
            print "The Machine now has", currentMachine.nodesNumber, "Gestalt nodes."

# The class for the Node tab
class wxNodeTabSetup(wxNodeTab.MyPanel1):

    def On_ChooseNodeType( self, event):
        global currentMachine
        currentNode = self.GetParent().GetSelection()
        currentType = self.m_radioBox1.GetSelection()
        if currentType == 0:
            print "Node #",currentNode+1,"is linear."
            currentMachine.machineNodes[currentNode].linear = True
            currentMachine.machineNodes[currentNode].rotary = False
        else:
            print "Node #",currentNode+1,"is rotary."
            currentMachine.machineNodes[currentNode].linear = True
            currentMachine.machineNodes[currentNode].rotary = False


# The class for the main app
class wxGestaltApp(wxMainApp.MyFrame1):

    def __init__(self, *args, **kw):
        super(wxGestaltApp, self).__init__(*args, **kw)
        global currentMachine
        self.InitUI()

    def InitUI(self):
        # Add Setup Tab
        self.tab_setup = wxTabSetup(self.m_notebook1)
        # Serial port setup
        self.tab_setup.m_listBox_serialPorts.Bind( wx.EVT_LISTBOX, self.On_ChooseSerialPort )
        SerialPortsAvailable = wxFunctions.ScanSerialPorts()
        self.tab_setup.m_listBox_serialPorts.Set(SerialPortsAvailable)
        # Baudrate setup
        self.tab_setup.m_listBox_baudrates.Set(wxMachines.baudratesListStrings)
        self.tab_setup.m_listBox_baudrates.SetSelection(16)
        self.tab_setup.m_listBox_baudrates.Bind( wx.EVT_LISTBOX, self.On_ChooseBaudrate )
        # Interface setup
        self.tab_setup.m_listBox_interfaceType.Set(wxMachines.interfacesList)
        self.tab_setup.m_listBox_interfaceType.SetSelection(0)
        self.tab_setup.m_listBox_interfaceType.Bind( wx.EVT_LISTBOX, self.On_ChooseInterface )
        # Add tab
        self.m_notebook1.AddPage(self.tab_setup, "Machine Setup", False )

        # Add Test Tab
        self.tab_test = wx.Panel(self.m_notebook1)
        self.m_notebook1.AddPage(self.tab_test, "Test the Machine", False )

        # Add CAM Tab
        self.tab_cam = wx.Panel(self.m_notebook1)
        self.m_notebook1.AddPage(self.tab_cam, "CAM job", False )

        # Show the app
        self.Show()

        # Starting the log
        # Redirect text here
        redir=RedirectText(self.wxLog)
        sys.stdout=redir

    def On_Quit( self, event ):
        self.Close(True)

    def On_ChooseSerialPort( self, event ):
        global currentMachine
        currentMachine.portName = event.GetString()
        print "Connecting to",currentMachine.portName,"..."

    def On_ChooseBaudrate( self, event ):
        global currentMachine
        currentMachine.baudRate = wxMachines.baudratesList[event.GetSelection()]
        print "Connecting with a baudrate of",currentMachine.baudRate,"..."

    def On_ChooseInterface( self, event ):
        global currentMachine
        currentMachine.interfaceType = wxMachines.interfacesList[event.GetSelection()]
        print "Connecting with the",currentMachine.interfaceType,"protocol..."

    def On_Message(self, title, content):
        # Open up a dialog
        dlg = wx.MessageDialog(self, content, title, wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':
    print wxMachines.baudratesList[16]
    ex = wx.App()
    ex1 = wxGestaltApp(None)
    ex1.Show()
    ex.MainLoop()
