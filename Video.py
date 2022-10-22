import re
from pytube import Playlist
import os
import time 
 # youtube-dl --recode-video mp4 https://www.youtube.com/watch?v=T8Zj1oLGaQE --output music.mp4

pl = "https://www.youtube.com/playlist?list=PLx2eSdPNcfW2fx7j71oI6vNyUGon-wvHm"

def execute():
    playlist = Playlist(pl)   

    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")    
    print(len(playlist.video_urls))    
    for url in playlist.video_urls:
        print(url)    
        time.sleep(15)
        os.system(f'youtube-dl --recode-video mp4 {url} --output video.mp4')
        time.sleep(10)
        os.system('py Upload.py')

execute()