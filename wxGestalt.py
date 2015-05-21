# -*- coding: utf-8 -*-

import wx
import wxClass


if __name__ == '__main__':
    ex = wx.App()
    ex1 = wxClass.MyFrame1(None)
    ex1.Show()
    ex.MainLoop()
