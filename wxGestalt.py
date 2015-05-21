# -*- coding: utf-8 -*-

import wx
import wxClass


class wxGestaltApp(wxClass.MyFrame1):

    def __init__(self, *args, **kw):
        super(wxGestaltApp, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.Show()

    def On_Quit( self, event ):
        self.Close(True)

    def On_ScanSerialPort( self, event ):
        event.Skip()


if __name__ == '__main__':
    ex = wx.App()
    ex1 = wxGestaltApp(None)
    ex1.Show()
    ex.MainLoop()
