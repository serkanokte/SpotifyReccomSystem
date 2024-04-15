import os
import django




os.environ.setdefault("DJANGO_SETTINGS_MODULE","musicsystem.settings")
django.setup()

import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
import librosa
import numpy as np
import matplotlib.pyplot as plt
from tracks.models import Track

CLIENT_ID ='...'
CLIENT_SECRET ='...'



# "6LPoTrXPOAufhzaiNnM4j0",
#    "2ZAvfw0KPr53Iqgnh6BQOn",
#    "2HCJEfZpe0HEtS7bcSKQyr",
#    "4OvtcLfv1ktFxVCKKGX1Qc",
#    "6D1BgK1Nhw8FWGd6797CV5",
#    "42zg2IA9F1Q7NcrOOMYdsI",
#    "27Dnms4t0x762FR11TILtv",
#    "2s3N3ooYpmZEtMDjB4Xf2i",
#    "3iVxcL5IfQrgV4J1qRrA4m",
#    "4wEg29ef5WR7sSRGeBzBXf"

playlist =["4FP5z455WSubn1O3vhxsy4",
           "7n7MLQO6JDfIsVrCJmtWwA",
           "7KOWYyeEQmfwHVaN2twQZO",
           "0U0tEIsfncpL9ZPOCYhsyx",
           "2NUpYRUzoMnEUzNZK7Pe3o",
           "5JA8pmbQsrNg2uuatJHKnU",
           "4ckI6JR2u7fY74zn9qNPZ0",
           "5Zo3WpFVKhTg0pHzsjvqSR",
           "3D52zgFEVOf17L3fGRcKYI",
           "1SB3MACpof5YtVtdtnoC9v",      
           ]



client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = sp.Spotify(client_credentials_manager = client_credentials_manager, requests_timeout=5, retries=3, status_retries=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])



def mfcc_func(path_wav,list_dict):

    ses_dizi, sr = librosa.load(path_wav, sr=None)
 

    mfccs = librosa.feature.mfcc(y=ses_dizi, sr=sr, n_mfcc=13)
    

    mean = np.mean(mfccs,axis=1)
    median = np.median(mfccs, axis=1)
    std = np.std(mfccs, axis=1)

    
    

    col_names = [f'mfccmean_{i}' for i in range(13)] + [f'mfccmedian_{i}' for i in range(13)] + [f'mfccstd_{i}' for i in range(13)]
    

    
    values = np.concatenate([mean, median, std])
    
    result_dict = dict(zip(col_names, values))

    list_dict.append(result_dict)
    
    # plt.figure(figsize=(10, 6))
    # librosa.display.specshow(mfccs)
    # plt.colorbar()
    # plt.xlabel('Zaman')
    # plt.ylabel('MFCC')
    # plt.show()

    
    






def get_playlist_tracks(playlist_id):   
    results = spotify.user_playlist_tracks("Serkan", playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])
    return tracks


def filter_important_audio_features(audio_features):
    feature_cols = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                    'liveness', 'valence', 'tempo']
    if audio_features is None or len(audio_features) == 0:
        return None
    return {k: audio_features[k] for k in feature_cols}




if __name__ == '__main__':
    
    

    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    track_directory = os.path.join(current_directory, "sarkilar2")
    
    
    wav_files = [file for file in os.listdir(track_directory) if file.endswith(".wav")]
    

    list_dict = []

    for wav_file in wav_files:
        wav_path = os.path.join(track_directory, wav_file)
        
        print(f"MFCC uygulaniyor: {wav_file}")
        mfcc_func(wav_path,list_dict)
    
    
    
    
    data = []
    

    totaltrack=0

    for i, playlist_id in enumerate(playlist):
        playlist_name = spotify.playlist(playlist_id)['name']
        tracks = get_playlist_tracks(playlist_id)
        num_tracks = len(tracks)
        totaltrack+=num_tracks
        


        
        track_ids = [track['track']['id'] for track in tracks]
        audio_features = []
        audio_features.extend(spotify.audio_features(track_ids))

        

        for j, track in enumerate(tracks):
            track_id = track['track']['id']
            track_name = track['track']['name']
            track_artist_name = track['track']['artists'][0]['name']
            track_audio_features = filter_important_audio_features(audio_features[j]) 
            track_genres = playlist_name
            track_popularity = track['track']['popularity']

            
        
           
            
            data.append({'id':track_id,'name':track_name,'artist':track_artist_name,
                         'genres':track_genres,**track_audio_features,'popularity':track_popularity})
    
    
    
    for dict1, dict2 in zip(data, list_dict):
        dict1.update(dict2)


    print(data) 
    

    

    for dict_track in data:
        track = Track(**dict_track)
        track.save()