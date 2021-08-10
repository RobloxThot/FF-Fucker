import subprocess as sp
import shlex, json, datetime


def getBitRate(file):
    """
    Gets the video bit rate and returns it as a JSON
    {
        'videoBitrate':videoBitRate,
        'audioBitrate':audioBitRate,
    }
    """
    # Get the video bitrate
    videoData = sp.run([
                        "ffprobe", "-v", "0", "-select_streams",
                        "v:0", "-show_entries", "stream=bit_rate",
                        "-of", "compact=p=0:nk=1", file], stdout=sp.PIPE).stdout
    videoDict = json.loads(videoData)  # Convert data from JSON string to dictionary
    videoBitRate = int(videoDict)  # Get the bitrate.
    
    # Get the audio bitrate
    audioData = sp.run([
                        "ffprobe", "-v", "0", "-select_streams",
                        "a:0", "-show_entries", "stream=bit_rate",
                        "-of", "compact=p=0:nk=1", file], stdout=sp.PIPE).stdout
    audioDict = json.loads(audioData)  # Convert data from JSON string to dictionary
    audioBitRate = int(audioDict)  # Get the bitrate.

    # Return both bitrates
    return {
        'videoBitrate':videoBitRate,
        'audioBitrate':audioBitRate,
    }

def getLength(filename):
    """
    Gives the length of the video in h:m:s
    """
    result = sp.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=sp.PIPE,
        stderr=sp.STDOUT)
    videoLength = round(float(result.stdout))
    return str(datetime.timedelta(seconds=videoLength))

def getFPS(filename):
    """
    Gives FPS of video back as a json
    {
        'rawFPS':rawFPS,
        'FPSFraction':FPSFraction,
    }
    """
    result = sp.run(f'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate "{filename}"',
        stdout=sp.PIPE,
        stderr=sp.STDOUT)
    FPSFraction = result.stdout.decode("utf-8").replace("\r\n", "")
    rawFPS = round(eval(FPSFraction),1)
    return {
        'rawFPS':rawFPS,
        'FPSFraction':FPSFraction,
    }

if __name__ == "__main__":
    videoLocation = input("Video file: ")
    bitrates = getBitRate(videoLocation.replace("\"", ""))
    videoLength = getLength(videoLocation.replace("\"", ""))
    FPS = getFPS(videoLocation.replace("\"", ""))
    print(f'video: {bitrates["videoBitrate"]}')
    print(f'audio: {bitrates["audioBitrate"]}')
    print(f'Length: {videoLength}')
    print(f'FPS: {FPS}')