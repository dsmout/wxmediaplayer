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