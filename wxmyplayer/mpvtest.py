

import mpv 

m= mpv.MPV()

url = "https://media-ssl.musicradio.com/HeartDance"

m.play(url)


# def h1(name,val):
#     print(name,val)

# @m.property_observer('metadata')
# def obs(name,val):
#     print(name,val)
# m.observe_property("metadata",h1)