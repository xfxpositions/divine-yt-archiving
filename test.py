import scrapetube

videos = scrapetube.get_channel("")

for video in videos:
    print(video['videoId'])