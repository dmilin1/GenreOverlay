import numpy as np
from .Database import Database
from .MP3Handler import MP3Handler
import random
import multiprocessing as mp
import time


class DataProvider:

    def __init__(self, q=None):
        self.q = q
        self.db = Database()
        self.currently_downloaded = MP3Handler().get_currently_downloaded()
        self.track_data = self.db.get_track_data(self.currently_downloaded)
        self.genres = self.db.get_all_genres()
        if q is not None:
            self.provide_data()
        

    def provide_data(self):
        mp3_handler = MP3Handler()
        pool = mp.pool.ThreadPool()

        while True:
            tracks_ids = random.sample(self.currently_downloaded, 8)
            track_data = pool.map(lambda track_id: mp3_handler.load_spectrogram(track_id), tracks_ids)
            

            return_data = {
                'inputs': [],
                'outputs': [],
            }

            for track in track_data:
                return_data['inputs'].append(track['data'])
                if len(self.track_data[track['id']]['genres']) > 0:
                    return_data['outputs'].append([ 1 if i == self.genres[self.track_data[track['id']]['genres'][0]] else 0 for i in range(len(self.genres)) ])
                else:
                    return_data['outputs'].append([ 1/len(self.genres) for i in range(len(self.genres)) ])
            
            return_data['inputs'] = np.array(return_data['inputs'])
            return_data['outputs'] = np.array(return_data['outputs'])

            self.q.put(return_data)

    def provide_all_data(self):
        mp3_handler = MP3Handler()
        pool = mp.pool.ThreadPool()

        track_data = pool.map(lambda track_id: mp3_handler.load_spectrogram(track_id), self.currently_downloaded)

        return_data = {
            'inputs': [],
            'outputs': [],
        }

        for track in track_data:
            if len(self.track_data[track['id']]['genres']) == 0:
                continue
            return_data['inputs'].append(np.mean(np.array(track['data']).T, axis=0))
            return_data['outputs'].append([ 1 if i == self.genres[self.track_data[track['id']]['genres'][0]] else 0 for i in range(len(self.genres)) ])

        random.shuffle(return_data['inputs'])
        random.shuffle(return_data['outputs'])

        return [return_data['inputs'], return_data['outputs']]