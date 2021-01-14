import wx,wx.media

class TestPanel(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None)
        self.testMedia = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        self.media = "http://funasia.streamguys1.com/live2"
        self.media = "track.mp3"
        self.testMedia.Bind(wx.media.EVT_MEDIA_LOADED, self.play)
        self.testMedia.Bind(wx.media.EVT_MEDIA_FINISHED, self.quit)
        if self.testMedia.Load(self.media):
            pass
        else:
            print("Media not found")
            self.quit(None)

    def play(self, event):
        self.testMedia.Play()

    def quit(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    Frame = TestPanel()
    Frame.Show()
    app.MainLoop()