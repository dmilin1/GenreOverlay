from .utilities.Database import Database
from .utilities.MP3Handler import MP3Handler
import requests
import boto3
import botocore
from blessed import Terminal
import time

term = Terminal()

db = Database()

all_tracks = db.get_all_track_ids()

currently_downloaded = MP3Handler().get_currently_downloaded()

tracks_to_download = list(filter(lambda track_id : track_id not in currently_downloaded, all_tracks))

s3 = boto3.resource('s3')

for i, track in enumerate(tracks_to_download):
    s3.Bucket('deezer-files-us-west-2').download_file(f'{track}.mp3', dl_location + f'{track}.mp3')

    percent_completed = ( i + len(currently_downloaded) ) / len(tracks_to_download)
    loading_bar = '[' + (''.join(['=' for _ in range(int(percent_completed*30))]) + '>').ljust(30) + ']'
    print(f"{term.clear}{loading_bar.ljust(35)}{'%.3f'%(100*percent_completed)}%{str(track).rjust(15)}.mp3")