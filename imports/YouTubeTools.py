import urllib.request, json, urllib

def getTitle(videoIdOrLink):
    """
    Get the title of a YouTube Video
    """

    #Check if its a ID or a link
    if "https://" in videoIdOrLink:
        videoLink = videoIdOrLink
    else:
        videoLink = "https://www.youtube.com/watch?v=%s" % videoIdOrLink

    #Setup to get the title i think (This was taken from stackoverflow)
    params = {"format": "json", "url": videoLink}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    #Send request to get the title
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return(data['title'])


if __name__ == "__main__":
    print(getTitle(input("Link: ")))