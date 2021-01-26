#!/bin/python3

import requests

url = "http://video.news.sky.com/snr/news/snrnews.mp3"

r= requests.get(url)
c = r.content

f= open("news11.mp3","wb")
f.write(c)
f.close()
