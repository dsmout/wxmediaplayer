import mutagen
def getLength(track):
    duration = track.info.length
    hr = int(duration // 3600)
    minSec = duration % 3600
    mins = int(minSec // 60)
    secs = int(minSec % 60)

    s_hr = str(hr).zfill(2)
    s_min = str(mins).zfill(2)
    s_sec = str(secs).zfill(2)
    if s_hr == "00":
        return s_min + ":" + s_sec
    else:
        return s_hr + ":" + s_min + ":" + s_sec

def getBitrate(track):
    bitrate = track.info.bitrate
    newBr = bitrate / 1000
    newBr = round(newBr)
    return newBr