#!/bin/python3

import argparse
import re
import subprocess

parser = argparse.ArgumentParser(description='Download the best quality video from YouTube.')
parser.add_argument('url', metavar='url', type=str, nargs='+', help='The URL to act on.')
parser.add_argument('-a', dest="audio", action='store_true', help='Download just the audio.')

detail_ex = r"^(?P<format>\d+)\s+(?P<extension>[a-z0-9]+)\s+(?P<resolution>\d+x\d+)\s+(?P<spec>\d+[ip])\s+" \
            r"(?P<bitrate>\d+k)\s+,\s+(?P<codecs>.+)$"

args = parser.parse_args()

url = args.url[0]

streams = subprocess.check_output(["youtube-dl", "-F", url], universal_newlines=True).split("\n")
audio_streams = [x for x in streams if "audio only" in x]
video_streams = [x for x in streams if "audio only" not in x]

if args.audio:
    for stream in audio_streams:
        stream_details = re.match(detail_ex, stream)
        if stream_details.group("extension") == "m4a":
            subprocess.run(["youtube-dl", "-f", stream_details.group("format"), url])

else:
    for stream in video_streams:
        if "(best)" in stream:
            stream_details = re.match(detail_ex, stream)
            if stream_details:
                fmt = stream_details.group("format")
                subprocess.run(["youtube-dl", "-f", fmt, url])
