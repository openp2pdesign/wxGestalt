# -*- coding: utf-8 -*-

# Modules
# Modules for the wx GUI
import wx
import GUI.wxMainApp as wxMainApp
import GUI.wxTabSetup as wxTabSetup
import GUI.wxNodeTab as wxNodeTab
import GUI.wxTabIdentify as wxTabIdentify
import GUI.wxTabTest as wxTabTest
import GUI.wxTabCAM as wxTabCAM
# Various functions
import Functions.wxFunctions as wxFunctions
# Module for log
import sys
# Module for Gestalt Machines
import Machines.wxMachines as wxMachines


# Variables
# The current machine edited in the app
currentMachine = wxMachines.wxMachine()
terminal = sys.stdout


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
            message = "The Machine now has " + str(currentMachine.nodesNumber) + " Gestalt node."
        else:
            message = "The Machine now has " + str(currentMachine.nodesNumber) + " Gestalt nodes."
        self.GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)

# The class for the Node tab
class wxNodeTabSetup(wxNodeTab.MyPanel1):

    def On_ChooseNodeType( self, event):
        global currentMachine
        currentNode = self.GetParent().GetSelection()
        currentType = self.m_radioBox1.GetSelection()
        if currentType == 0:
            message = "Node #" + str(currentNode+1) + " is linear."
            self.GetParent().GetParent().GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)
            currentMachine.machineNodes[currentNode].linear = True
            currentMachine.machineNodes[currentNode].rotary = False
        else:
            message = "Node #" + str(currentNode+1) + " is rotary."
            self.GetParent().GetParent().GetParent().GetParent().m_statusBar1.SetStatusText(message, 0)
            currentMachine.machineNodes[currentNode].linear = True
            currentMachine.machineNodes[currentNode].rotary = False


# The class for the Identify tab
class wxTabIdentify(wxTabIdentify.MyPanel1):

    def __init__(self, *args, **kw):
        super(wxTabIdentify, self).__init__(*args, **kw)
        global currentMachine
        self.InitUI()

    def InitUI(self):
        # Starting the log
        # Redirect text here
        self.redir=RedirectText(self.wxLog)
        sys.stdout=self.redir
        print "-------------------------------------------------------------------------------"
        print "Please identify each Gestalt node by pressing on their buttons when asked here:"
        print


# The class for the CAM tab
class wxTabCAM(wxTabCAM.MyPanel1):

    def On_LoadFile( self, event ):
        self.m_textCtrl1.SetStatusText("pippo")

    def On_SaveCAM( self, event ):
        event.Skip()

    def On_LaunchCAM( self, event ):
        event.Skip()


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
        self.m_notebook1.AddPage(self.tab_setup, "1. Machine Setup")

        # Add Identify Tab
        self.tab_identify = wxTabIdentify(self.m_notebook1)
        self.m_notebook1.AddPage(self.tab_identify, "2. Identify the nodes")

        # Add Test Tab
        self.tab_test = wxTabTest.MyPanel1(self.m_notebook1)
        self.m_notebook1.AddPage(self.tab_test, "3. Test the Machine")

        # Add CAM Tab
        self.tab_cam = wxTabCAM(self.m_notebook1)
        self.m_notebook1.AddPage(self.tab_cam, "4. CAM")

    def On_Quit( self, event ):
        self.Close(True)

    def On_ChooseSerialPort( self, event ):
        global currentMachine
        currentMachine.portName = event.GetString()
        message = "Connecting to " + currentMachine.portName + " ..."
        self.m_statusBar1.SetStatusText(message, 0)

    def On_ChooseBaudrate( self, event ):
        global currentMachine
        currentMachine.baudRate = wxMachines.baudratesList[event.GetSelection()]
        message = "Connecting with a baudrate of ",currentMachine.baudRate,"..."
        self.m_statusBar1.SetStatusText(message, 0)

    def On_ChooseInterface( self, event ):
        global currentMachine
        currentMachine.interfaceType = wxMachines.interfacesList[event.GetSelection()]
        message = "Connecting with the ",currentMachine.interfaceType," protocol..."
        self.m_statusBar1.SetStatusText(message, 0)

    def On_SelectNotebookPage( self, event):
        currentMainTab = event.GetSelection()
        event.Skip()

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
