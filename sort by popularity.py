import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth

#INTIIAL VARS TO CALL API
PLAYLIST_ID = 'YOUR-PLAYLIST-ID-HERE'

#scope for api
scope = 'playlist-modify-public'

#MAKE SURE YOU MAKE THE ENVIRONMENT VARS
spotifyObject = sp.Spotify(auth_manager=SpotifyOAuth(scope=scope)) 

print('obj made')

#FIRST PLAYLIST
TRACKS = spotifyObject.playlist_items(PLAYLIST_ID, offset=0)

#playlist song total
playlist_size = TRACKS['total']

print('tracks acquired')

#DICTIONARY OF SONG IDS TO POPULARITY
playlist_dict = {}

#OFFSET TRACKER
offset_var = 0

#Loops over all playlist songs and reacts to the offset change

#basically splits the offset into units of 100 so depending on 
#how many hundreds the total playlist has will determine how many loops it goes through
while offset_var // 100 <= TRACKS['total'] // 100:
    print(f'processing playlist block {offset_var // 100 + 1}...')
    #loops over the 100 songs queued in
    for song in range(len(TRACKS['items'])):
        #link the track uri to the popularity rating in the dict
        try:
            playlist_dict[TRACKS['items'][song]['track']['uri']] = TRACKS['items'][song]['track']['popularity']
        #if the song is invalid dont factor it in
        except:
            pass
    
    #queues into the next 100 songs
    offset_var += 100

    #changes tracks to the new queue
    TRACKS = spotifyObject.playlist_items(PLAYLIST_ID, offset=offset_var)

#it is done
print('playlist analyzed')
sorted_playlist_dict = dict(sorted(playlist_dict.items(), key=lambda x: x[1]))

print([list(sorted(playlist_dict.items(), key=lambda x: x[1]))[i] for i in range(-1,-101,-1)])
