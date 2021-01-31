import requests

def getUrl(url2):
    myurl = url2
    # qmpos = myurl.find("?")
    # if qmpos != -1:
    #     myurl = myurl[0:qmpos]
    r = requests.get(myurl)
    c = r.content.decode("utf-8")
    lastslash = myurl.find("/")
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
                myurl = baseurl + j
            else:
                myurl = j
            getUrl(myurl)
        elif j.endswith(".mp3") or j.endswith(".aac"):
            out.append(j)
    print("me", out)
    # return out


if __name__ == "__main__":
    u = "https://media.radiojackie.com/redirector/frontend.m3u8"
    getUrl(u)