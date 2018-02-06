from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import time
import spotipy

client_credentials_manager = SpotifyClientCredentials('62282555af7347fd92b608d7d2daf1d9','6a927564cd03483fba5eb814b42e8f8e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class spyscraper:
    def __init__(self,outputid):
        self.artist_ids = []
        self.artist_names = []
        self.album_ids = []
        self.album_names = []
        self.track_ids = []
        self.track_names = []
        self.track_analysis = []
        self.outputid = outputid
    
    def findArtists(self, lim, maxPage, q_value):
        for i in range(maxPage):
            results = sp.search(q=q_value,type='artist',limit=lim,offset=i*lim)
            artists = results['artists']['items']
            for j in range(len(artists)):
                self.artist_ids.append(artists[j]['id'])
                self.artist_names.append(artists[j]['name'])
                print('Got',artists[j]['name'])

    def findAlbums(self):
        for i in range(len(self.artist_ids)):
            results = sp.artist_albums(self.artist_ids[i],album_type='album')
            albums = results['items']
            print(albums)
            for j in range(len(albums)):
                if albums[j]['name'] not in self.album_names:
                    self.album_ids.append(albums[j]['id'])
                    self.album_names.append(albums[j]['name'])
                    print('Got',albums[j]['name'])

    def findTracks(self):
        for i in range(len(self.album_ids)):
            results = sp.album(self.album_ids[i])
            tracks = results['tracks']['items']
            current_tracks = []
            for j in range(len(tracks)):
                current_tracks.append(tracks[j]['id'])
                self.track_ids.append(tracks[j]['id'])
                self.track_names.append(tracks[j]['name'])
                print('Got',tracks[j]['name'])
            self.findTrackAnalysis(current_tracks)

    def findTrackAnalysis(self,track_ids):
        results = sp.audio_features(track_ids)
        for i in range(len(results)):
            try:
                single_track_analysis = [results[i]['energy'],results[i]['liveness'],results[i]['valence'],results[i]['time_signature'],
                                  results[i]['danceability'],results[i]['instrumentalness'],results[i]['tempo'],results[i]['loudness'],
                                  results[i]['mode'],results[i]['key'],results[i]['acousticness'],results[i]['speechiness']]
                self.track_analysis.append([single_track_analysis],[self.outputid])
                print(single_track_analysis)
            except TypeError:
                print('Oops!')

