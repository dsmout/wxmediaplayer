#!/usr/bin/env python
import os
import time
import wx,wx.media
# import wx.lib.buttons as buttons

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
         wx.Frame.__init__(self, parent, -1, title, pos=(150,150), size=(640, 480),
                          style=wx.MAXIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
            self.CreateStatusBar() # status bar
            filemenu = wx.Menu()
 
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About", "Info about this app")
        filemenu.AppendSeparator()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open File")
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit" , "Terminate")

       

        # menubar
        mb = wx.MenuBar()
        mb.Append(filemenu,"&File")
        self.SetMenuBar(mb) # add to frame

        #events

        self.Bind(wx.EVT_MENU,self.onAbout,menuAbout)
        self.Bind(wx.EVT_MENU,self.onOpen,menuOpen)
        self.Bind(wx.EVT_MENU,self.onExit,menuExit)

        self.Show(True)


     def onAbout(self,e):
        dlg = wx.MessageDialog(self, "A simple Player","A small Player", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


    def onExit(self,e):
        self.Close(True)



app = wx.App(False)
frame =MyFrame(None,"Small Player")
app.MainLoop()

