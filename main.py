from pytube import YouTube
from pytube import Channel
import os
import json
import scrapetube
import re
import time

channel_link = 'https://www.youtube.com/c/TolgaTurann/videos'
c = Channel(channel_link)
videos_count = 0
url_base = "https://www.youtube.com/watch?v="
videos_dir_main = os.path.join(os.getcwd(), "videos")
output_dir = os.path.join(videos_dir_main, c.channel_name)


def create_directories(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '_', filename)

def download_video_from_id(id: str, output_dir):
   create_directories(output_dir) # Create the necessary directories
   

   global videos_count
   url = f"{url_base}{id}" 
   try:
      yt = YouTube(url)
   except Exception as e: 
      print(f'Video {url} is unavaialable because of {e}, skipping.')
      return
   
   video_title = yt.title
   video_date = yt.publish_date.strftime("%d/%m/%Y, %H:%M:%S")
   video_views = yt.views
   
   # creating folder for video streams und json
   output_file_dir = os.path.join(output_dir, sanitize_filename(f"{video_title}.{id}"))
   os.mkdir(output_file_dir)
   
   
   
   video_json = json.dumps({
      video_title: video_title,
      video_date: video_date,
      video_views: video_views
   }, ensure_ascii=False).encode("utf-8")
   
   video_json_file_path= os.path.join(output_file_dir, sanitize_filename(f"{video_title}.{id}.json"))
   with open(video_json_file_path, "w", encoding="utf-8") as outfile:
      # we need to decode the utf-8 bytes
      
      outfile.write(video_json.decode())
      print(f"{video_json} writed to {video_json_file_path}")
   
   

   # i know this a poor code, i'll fix it. if you still seeing this from the future, sorry about that.

   try:

      
      res = yt.streams.get_lowest_resolution().resolution
      output_file_name = sanitize_filename(f"{video_title}.{id}.{res}.mp4") 
      output_file_path = os.path.join(output_file_dir, sanitize_filename(output_file_name) ) 
      yt.streams.get_lowest_resolution().download(output_path=output_file_dir, filename=sanitize_filename(f"{video_title}.{id}.{res}.mp4"))
      print(output_file_name)
      
      
      res = "720p"
      output_file_name = f"{video_title}.{id}.{res}.mp4"
      output_file_path = os.path.join(output_file_dir, sanitize_filename(output_file_name) )
      print(output_file_name)
      yt.streams.get_by_resolution("720p").download(output_path=output_file_dir, filename= sanitize_filename(f"{video_title}.{id}.{res}.mp4") )

      videos_count += 1
      print(f"videos count is now {str(videos_count)}")
   except Exception as e: 
      print(f"some error occured in downloading video of {id}, err: {e}")
      return
   else:
      print(f"video {id} downloaded to {output_file_path}")
      
   

def check_channel(c: Channel):
   channel_id = c.channel_id
   videos_raw = scrapetube.get_channel(channel_id)

   for video in videos_raw:
      id = video['videoId']
      download_video_from_id(id, output_dir)
      print(id)
   print(videos_count)
   
#currently no need to asyncio, it can be run sync (idk the future)


while True:
   
   # checks channel, if there is any videos, downloads them all
   check_channel(c)
   #default 5400 sec
   time.sleep(1)

