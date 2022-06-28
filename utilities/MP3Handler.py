import librosa
from os import listdir
import random
import numpy as np
import pickle
from blessed import Terminal


class MP3Handler:

    sample_rate = 22050
    segment_seconds = 15

    def __init__(self):
        self.dl_location = 'F:/Datasets/music/'
        self.spectrogram_location = 'F:/Datasets/spectrograms/'

    def load_mp3(self, track_id):
        num_of_seconds = librosa.get_duration(filename=self.dl_location + track_id + '.mp3')//1
        start_time = random.randint(0, num_of_seconds - MP3Handler.segment_seconds - 1)
        data = librosa.load(self.dl_location + track_id + '.mp3', offset=start_time, duration=MP3Handler.segment_seconds)[0]
        S = librosa.feature.mfcc(data, n_mfcc=40)
        return {
            'id': track_id,
            'data': S,
        }
    
    def load_spectrogram(self, track_id):
        with open(self.spectrogram_location + track_id + '.pickle', 'rb') as file:
            return pickle.load(file)

    def get_currently_downloaded(self):
        return list(map(lambda file : file.split('.')[0], listdir(self.dl_location)))
    
    def generate_spectrograms(self):
        print('converting mp3s to spectrograms')
        existing_spectrograms = list(map(lambda file : file.split('.')[0], listdir(self.spectrogram_location)))
        currently_downloaded = self.get_currently_downloaded()
        term = Terminal()
        for i, track in enumerate(currently_downloaded):
            if track not in existing_spectrograms:
                with open(self.spectrogram_location + track + '.pickle', 'wb') as file:
                    pickle.dump(self.load_mp3(track), file)
                    percent_completed = ( i + len(existing_spectrograms) ) / (len(currently_downloaded) - len(existing_spectrograms))
                    loading_bar = '[' + (''.join(['=' for _ in range(int(percent_completed*30))]) + '>').ljust(30) + ']'
                    print(f"{term.clear}{loading_bar.ljust(35)}{'%.3f'%(100*percent_completed)}%{str(track).rjust(15)}.mp3")



# import matplotlib.pyplot as plt
# import numpy as np
# import librosa.display

# for track in MP3Handler().get_currently_downloaded():

#     S = MP3Handler().load_mp3(track)['data']

#     print(S)
#     print(np.shape(S))


#     fig, ax = plt.subplots()
#     img = librosa.display.specshow(S, x_axis='time', ax=ax)
#     ax.set_title('Power spectrogram')
#     fig.colorbar(img, ax=ax, format="%.2f amplitude")

#     plt.show()



MP3Handler().generate_spectrograms()