#!/usr/bin/python3
import wx
import os
import mpv
import requests
import time
import subprocess
import mutagen

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
        # menuRstop = filemenu.Append(wx.ID_ANY,"&RecS", "Rstop")

       

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
        self.Bind(wx.EVT_MENU, self.onRecord,menuRec)
        # self.Bind(wx.EVT_MENU, self.recStop,menuRstop)

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

    def onPlay(self, e):
        if self.playing:
            self.mpvAudio.stop()
            self.playing =False
        else:
            self.mpvAudio.play(self.url1)
            self.playing = True

    def getUrl(self):
        myurl = self.url1
        r = requests.get(myurl)
        c = r.content.decode("utf-8")
        lastslash = myurl.rfind("/")
        baseurl = myurl[0:lastslash]
        baseurl = baseurl + "/"
        sep = "\n"
        out = []
        if "\r\n" in c:
            sep = "\r\n"
        c= c.split(sep)
        for j in c:
            if j.endswith(".m3u8"):
                if not j.startswith("http"):
                    j= baseurl + j
                r= requests.get(j)
                c = r.content.decode("utf-8")
                c =c.split(sep)
            elif j.endswith(".mp3") or j.endswith(".aac"):
                if not j.startswith("http"):
                    j= baseurl + j
                out.append(j)
        
        if len(out) ==0:
            # print("2nd go")
            for k in c:
                if k.endswith(".mp3") or k.endswith(".aac"):
                    if not k.startswith("http"):
                        k= baseurl + k
                    out.append(k) 
        return out

    def recM3u8(self):
        if self.recording:
            chunks = getUrl(self)
            try:
                self.recFile =open("stream97.aac","ab")
            except:
                print("file trouble")
            for c in chunks:
                r = requests.get(c)
                c = r.content
                self.recFile.write(c)
            while self.recording:
                time.sleep(10)
                newChunkUrl = getUrl(self)[-1]
                reqNewChunk = requests.get(newChunkUrl)
                newChunk = reqNewChunk.content
                self.recFile.write(newChunk) 

    def recNorm(self):
        fp = subprocess.check_output(["ffprobe",self.url1],stderr=subprocess.STDOUT)
        fp = fp.decode("utf-8")
        fName = ""
        if "Audio: aac" in fp:
            fName = "stream97.aac"
        elif "Audio: mp3" in fp:
            fName = "stream97.mp3"    
        try:
            self.recFile =open(fName,"wb")
        except:
            print("file issue")

        while self.recording:
            r= requests.get(self.url1, stream=True)
            for block in r.iter_content(1024):
                self.recFile.write(block)
        self.recFile.close()

            # try:
            #     self.recFile =open(fName,"wb")
            #     # for block in r.iter_content(1024):
            #             # f.write(block) 
            #             # if not self.recording:
            #             #     break

        
    def onRecord(self,e):
        myurl = self.url1
        if not self.recording:
            if ".m3u8" in myurl:
                self.recording = True
                self.recM3u8()
            else:
                self.recording = True
                self.recNorm()

        elif self.recording:
            self.recording = False



    # def onRecord(self , e):
    #     myurl = self.url1
    #     self.recording = True
    #     if "m3u8" in myurl:
    #         self.recM3u8(self)
    #     else:
    #         self.recNorm(self)
    
app = wx.App(False)
frame =MyFrame(None,"Small Player")
app.MainLoop()




