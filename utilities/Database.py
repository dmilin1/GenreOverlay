import pymongo
from bson.objectid import ObjectId

class Database:

    __instance = None

    @staticmethod 
    def getInstance():
        if Database.__instance == None:
            Database.__instance = Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance != None:
            raise Exception("This class is a singleton!")

        client = pymongo.MongoClient('db_link')
        self.db = client['Auth']
    
    def get_all_track_ids(self):
        return list(map(lambda track: track['deezerId'], self.db['tracks'].aggregate([
            {
                '$match': {
                    'deezerId': {
                        '$ne': None
                    }
                }
            }, {
                '$project': {
                    'deezerId': True
                }
            }
        ])))

    def get_all_genres(self, depth = 0):
        genres = map(lambda track: track['_id'], self.db['tracks'].aggregate([
            {
                '$match': {
                    'deezerId': {
                        '$ne': None
                    }
                }
            }, {
                '$project': {
                    'genre': {
                        '$arrayElemAt': [
                            '$genres', depth
                        ]
                    }
                }
            }, {
                '$match': {
                    'genre': {
                        '$ne': None
                    }
                }
            }, {
                '$group': {
                    '_id': '$genre'
                }
            }
        ]))
        genre_obj = {}
        for i, genre in enumerate(genres):
            genre_obj[genre] = i
        return genre_obj

    def get_track_data(self, track_ids):
        rawData = self.db['tracks'].aggregate([
            {
                '$match': {
                    'deezerId': {
                        '$ne': None,
                    },
                    'deezerId': {
                        '$in': track_ids
                    },
                }
            }, {
                '$project': {
                    'deezerId': True, 
                    'genres': True, 
                    'moods': True
                }
            }
        ])
        track_data = {}
        for track in rawData:
            track_data[track['deezerId']] = {
                'genres': track['genres'],
                'moods': track['moods']
            }
        return track_data
