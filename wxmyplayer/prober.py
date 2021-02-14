import subprocess

fp = subprocess.check_output(["ffprobe","https://media-ssl.musicradio.com/HeartDance"],stderr=subprocess.STDOUT)
fp = fp.decode("utf-8")

lines = fp.split("\n")

importantLines = [l for l in lines if "icy-name" in l or "StreamTitle" in l]
z = "\n".join(importantLines)
print(z)