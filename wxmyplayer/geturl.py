import requests,time

def getUrl(url2):
    myurl = url2
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

def recM3u8(url,recording):
        if  recording:
            chunks = getUrl(url)
            recFile = None
            try:
                recFile =open("stream97.aac","ab")
            except:
                print("file trouble")
            for c in chunks:
                r = requests.get(c)
                c = r.content
                recFile.write(c)
            while recording:
                time.sleep(10)
                newChunkUrl = getUrl(url)[-1]
                reqNewChunk = requests.get(newChunkUrl)
                newChunk = reqNewChunk.content
                recFile.write(newChunk) 

if __name__ == "__main__":
    u = "https://admdn7ta.cdn.mangomolo.com/rdo1/rdo1.stream_aac/playlist.m3u8?stime=20210124103003&etime=20210131182323&token=09d02d17120065004796b"
    recM3u8(u,True)