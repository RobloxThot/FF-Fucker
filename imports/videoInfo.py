import subprocess as sp
import shlex
import json


def getBitRate(file):
    # Build synthetic video for testing:
    ################################################################################
    sp.run(shlex.split(f'ffmpeg -y -f lavfi -i testsrc=size=320x240:rate=30 -f lavfi -i sine=frequency=400 -f lavfi -i sine=frequency=1000 -filter_complex amerge -vcodec libx264 -crf 17 -pix_fmt yuv420p -acodec aac -ar 22050 -t 10 tempfiles/{file}'))
    ################################################################################

    # Use FFprobe for 
    # Execute ffprobe (to get specific stream entries), and get the output in JSON format
    data = sp.run(shlex.split(f'ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -print_format json tempfiles/{file}'), stdout=sp.PIPE).stdout
    dict = json.loads(data)  # Convert data from JSON string to dictionary
    bit_rate = int(dict['streams'][0]['bit_rate'])  # Get the bitrate.

    return f'bit_rate = {bit_rate}'