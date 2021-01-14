#!/usr/bin/python3
import wx  # wx.media
import os
import mpv
import requests
import time
import subprocess

class MyFrame(wx.Frame):
# derive frame class
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title, size=(300,300))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,10,style=wx.ALIGN_CENTER)
        # label.SetLabel("Duration")
        font = wx.Font(8, wx.ROMAN, wx.ITALIC, wx.NORMAL) 
        lbl.SetFont(font) 
        lbl.SetLabel("me") 
        box.Add(lbl,20,wx.ALIGN_CENTER)

        self.url1 = "http://funasia.streamguys1.com/live3"
        self.mpvAudio = mpv.MPV()
        # self.mpvAudio.play(self.url1)  
        self.playing = False
        self.CreateStatusBar() # status bar
        self.elapsed = ""
        self.recFile = None
        self.recording = False
        btn = wx.Button()

        @self.mpvAudio.property_observer('time-pos')
        def time_observer(name,val):

            try:
                wholeSecs = round(val)
            except:
                wholeSecs = 0
            sep = ":"
            hr = 0
            min1 = 0
            sec = 0
            elapsedTemp = ""

            if wholeSecs < 3600:
                min1 = wholeSecs // 60
                sec = wholeSecs % 60
                elapsedTemp = str(min1)+ sep + str(sec).zfill(2)
                #print("Debug ",elapsed)
            elif wholeSecs >= 3600:
                hr = wholeSecs // 3600
                lo = wholeSecs % 3600
                if lo < 60:
                    min1 = lo //60
                    sec = lo %60
                else: 
                    sec = lo
                elapsedTemp = str(hr) + sep + str(min1).zfill(2) + sep + str(sec).zfill(2)

            if elapsedTemp != self.elapsed:
                self.elapsed = elapsedTemp
                print("Now Playing at: ",self.elapsed)


        filemenu = wx.Menu()
 
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About", "Info about this app")
        filemenu.AppendSeparator()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open File")
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit" , "Terminate")
        # menuStop = filemenu.Append(wx.ID_STOP, "&Stop" ,"Stop")
        menuPlay = filemenu.Append(wx.ID_ANY, "&Play", "Play")
        menuRec = filemenu.Append(wx.ID_ANY,"&Rec", "Record")
        menuRstop = filemenu.Append(wx.ID_ANY,"&RecS", "Rstop")

       

        # menubar
        mb = wx.MenuBar()
        mb.Append(filemenu,"&File")
        self.SetMenuBar(mb) # add to frame

        #events

        self.Bind(wx.EVT_MENU,self.onAbout,menuAbout)
        self.Bind(wx.EVT_MENU,self.onOpen,menuOpen)
        self.Bind(wx.EVT_MENU,self.onExit,menuExit)
        # self.Bind(wx.EVT_MENU,self.onStop,menuStop)
        self.Bind(wx.EVT_MENU,self.onPlay,menuPlay)
        self.Bind(wx.EVT_MENU, self.recStartStop,menuRec)
        self.Bind(wx.EVT_MENU, self.recStop,menuRstop)

        self.Show(True)
        

    def onAbout(self,e):
        dlg = wx.MessageDialog(self, "A simple Editor","A small Editor", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


    def onExit(self,e):
        self.Close(True)
    
    def onOpen(self, e):
        self.dirname = ""
        dlg = wx.FileDialog(self, "Choose File", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            fullname = os.path.join(self.dirname,self.filename)
            self.mpvAudio.play(fullname)
            self.playing = True
        dlg.Destroy()

    # def onStop(self, e):
    #     self.mpvAudio.stop()

    def onPlay(self, e):
        if self.playing:
            self.mpvAudio.stop()
            self.playing =False
        else:
            self.mpvAudio.play(self.url1)
            self.playing = True
    
    def recStartStop(self,e):
            if not self.recording:
                r= requests.get(self.url1, stream=True)
                try:
                    self.recFile =open("stream97.mp3","wb")
                    for block in r.iter_content(1024):
                            f.write(block) 
                            if self.recording:
                                break
                except:    
                    pass

    def recStop(self , e):
        self.recording = True
        self.recFile.close()

app = wx.App(False)
frame =MyFrame(None,"Small Player")
app.MainLoop()




