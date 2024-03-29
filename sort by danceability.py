#the goal is to identify the top 100 most danceable songs in my playlist
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth

#PLAYLIST THAT IS ANALYZED
PLAYLIST_ID = 'YOUR-PLAYLIST-ID-HERE'

#PLAYLIST THAT IS BEING ADDED TO (just make a blank playlist)
PLAYLIST_ID2 = 'YOUR-PLAYLIST-ID-HERE'

#YOURE SPOTIFY USERNAME
USERNAME = 'YOUR-SPOTIFY-USERNAME-HERE'

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

#LIST OF ALBUM COVERS
playlist_dict = {}

#OFFSET TRACKER
offset_var = 0

#test code to see if it prints the danceability
# ids = [TRACKS['items'][song]['track']['id'] for song in range(len(TRACKS['items']))]
# print(TRACKS['items'][0]['track']['id'])
# print(spotifyObject.audio_features('2H4lcD1vrTlkwny6GlJszg'))

#I make a txt file just to in case Spotify API runs out of calls and I want to store what I've called already
f = open('dance.txt','w')

# Loops over all playlist songs and reacts to the offset change

# basically splits the offset into units of 100 so depending on 
# how many hundreds the total playlist has will determine how many loops it goes through
while offset_var // 100 <= TRACKS['total'] // 100:
    print(f'processing playlist block {offset_var // 100 + 1}...')
    #loops over the 100 songs queued in
    for song in range(len(TRACKS['items'])):
        #link the track uri to the danceability rating in the dict
        try:
            playlist_dict[TRACKS['items'][song]['track']['uri']] = spotifyObject.audio_features(TRACKS['items'][song]['track']['id'])[0]['danceability']
            print('added')
        #if the song is invalid dont factor it in
        except:
            pass
    
    #queues into the next 100 songs
    offset_var += 100

    #changes tracks to the new queue
    TRACKS = spotifyObject.playlist_items(PLAYLIST_ID, offset=offset_var)

#write the data collected to the txt
f.write(str(playlist_dict))

#it is done with receiving the playlist data
print('playlist analyzed')

#sorts the dict by danceability
sorted_playlist_dict = dict(reversed(sorted(playlist_dict.items(), key=lambda x: x[1])))

#write this newly sorted data
f.write('/n' + str(sorted_playlist_dict))
f.close()

#just a placeholder number (100); this should yield about 3 hours of songs.
#Note: setting this higher could result in a "Max Reentries" Spotify API error meaning you will be restricted from sending API requests for 13 hours
playlist_bound = 100 #INCREASE FOR LONGER PLAYLIST

#if the playlist is more than 100 just add the top 100
if len(sorted_playlist_dict) > playlist_bound:
    print([list(sorted_playlist_dict)[i] for i in range(playlist_bound)])
    spotifyObject.user_playlist_add_tracks(user= USERNAME, playlist_id = PLAYLIST_ID2, tracks = [list(sorted_playlist_dict)[i] for i in range(playlist_bound)])

#just add what's in the playlist if less than 100 in danceability order
else:
    print([list(sorted_playlist_dict)[i] for i in range(len(sorted_playlist_dict))])
    spotifyObject.user_playlist_add_tracks(user= USERNAME, playlist_id = PLAYLIST_ID2, tracks = [list(sorted_playlist_dict)[i] for i in range(len(sorted_playlist_dict))])