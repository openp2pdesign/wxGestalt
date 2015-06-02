# -*- coding: utf-8 -*-

import wx
import wx.stc as stc

# Platform variables
if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Anivers',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
elif wx.Platform == '__WXMAC__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Monaco',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 12,
              'size2': 10,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }


# A class for a code editor with style
class codeEditor(stc.StyledTextCtrl):

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.Size( 880,530 ),style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)

        # Zoom keys
        self.CmdKeyAssign(ord('+'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        # Config
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetViewWhiteSpace(True)
        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)
        self.SetViewEOL(False)
        self.SetEOLMode(stc.STC_EOL_CRLF)
        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()
        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,"fore:#000000,back:#ab9c9c,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")

        # Python styles
        # Indentation
        self.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")
        # Default
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:'%(helv)s',size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,back:#F0FFF0,face:%(other)s,size:%(size)d")
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#c21d76,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#c2451d,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#c2451d,face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,back:#f7ede1,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,back:#f7ede1,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,back:#F0FFF0,size:%(size)d" % faces)
        # Selection
        self.SetSelBackground(1, '#66CCFF')
        self.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
