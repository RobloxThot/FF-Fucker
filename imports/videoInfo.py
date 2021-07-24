import subprocess as sp
import shlex, json, datetime


def getBitRate(file):
    # Build synthetic video for testing:
    ################################################################################
    sp.run(shlex.split(f'ffmpeg -y -f lavfi -i testsrc=size=320x240:rate=30 -f lavfi -i sine=frequency=400 -f lavfi -i sine=frequency=1000 -filter_complex amerge -vcodec libx264 -crf 17 -pix_fmt yuv420p -acodec aac -ar 22050 -t 10 {file}'))
    ################################################################################

    # Use FFprobe for 
    # Execute ffprobe (to get specific stream entries), and get the output in JSON format
    data = sp.run(shlex.split(f'ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -print_format json {file}'), stdout=sp.PIPE).stdout
    dict = json.loads(data)  # Convert data from JSON string to dictionary
    bit_rate = int(dict['streams'][0]['bit_rate'])  # Get the bitrate.

    return f'bit_rate = {bit_rate}'

def getLength(filename):
    result = sp.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=sp.PIPE,
        stderr=sp.STDOUT)
    videoLength = round(float(result.stdout))
    return str(datetime.timedelta(seconds=videoLength))

if __name__ == "__main__":
    print(getBitRate(r"C:\Users\Owner\Downloads\1560344_alternate_116437.720p.mp4"))
    print(getLength(r"C:\Users\Owner\Downloads\1560344_alternate_116437.720p.mp4"))