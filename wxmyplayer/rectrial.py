import requests
def main():
    surl = "http://funasia.streamguys1.com/live3"

    r = requests.get(surl,stream=True)
    f= None
    try:
        f = open("stream97.mp3","wb")
        for block in r.iter_content(1024):
            f.write(block)
    except KeyboardInterrupt:
        f.close()
            

    
if __name__ == "__main__":
    main()