import wx 
import wx.media
 
class MyFrame(wx.Frame): 
    def __init__(self,parent,title): 
        wx.Frame.__init__(self, parent, -1, title, pos=(150,150), size=(640, 480),
                          style=wx.MAXIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.Bind(wx.EVT_CLOSE,self.OnCloseWindow)
        panel = wx.Panel(self,size=(350,200)) 
        video = wx.media.MediaCtrl(panel, -1, fileName=r"track.mp3",
                                   pos=wx.Point(100,50),size=wx.Size(320,240))
 
        video.ShowPlayerControls(flags = wx.media.MEDIACTRLPLAYERCONTROLS_STEP)                
        video.Play()
 
    def OnCloseWindow(self,event): 
        self.Destroy()
 
class MyApp(wx.App): 
    def OnInit(self): 
        frame = MyFrame(None,'Form1') 
        frame.Show(True) 
        return True 

app=MyApp(redirect=True) 
app.MainLoop()