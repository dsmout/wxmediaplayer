#!/usr/bin/python3

import mpv
player = mpv.MPV(ytdl=False)
player['vid'] = 'no'

@player.property_observer('time-pos')
def time_observer(_name, value):
  # Here, _value is either None if nothing is playing or a float containing
  # fractional seconds since the beginning of the file.
  # print('Now playing at {:.2f}s'.format(value))
  print('Now playing at ', str(value))

player.play('track.mp3')
player.wait_for_playback()    