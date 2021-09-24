from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Songs
from .models import Playlist
from .models import User
from .models import userPlaylist
from . import db
import json


pplay = Blueprint('pplay', __name__)



import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import csv
#import pandas as pd
from pprint import pprint


client_id='079ba6fc4dc948dbaed185422351ca25'
client_secret='2e95bdb6aab3416cac2a948ca4acf26a'
redirect_uri='http://localhost:8888/callback'
scope='user-library-read'

token = util.prompt_for_user_token(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
tester = []

#takes an artists name
#this triggers the rest of the program.
#take the first public album available and pull those songs
'''This function is for users that do have a Spotify account.'''
def get_playlist_tracks(username, playlist_id):
    sp = spotipy.Spotify(auth=token)
    results = sp.user_playlist_tracks(username, playlist_id)
    print("test")
    tracks_user = results['items']
    while(results['next']):
        results = sp.next(results)
        tracks_user.extend(results['items'])
    print("test")
    return (create_dict(tracks_user))
    
'''this function is only for public user.'''
def get_playlist_tracks_uri(playlist_id):
    xp = spotipy.Spotify(auth=token)
    results = xp.playlist(playlist_id)
    tracks_user = results['tracks']['items']
    return(create_dict(tracks_user))

'''input is a string entry.'''
def artist_entry(artist):
    input = artist
    sp = spotipy.Spotify(auth=token)
    artist_search = sp.search(q=input, type='playlist')
    result_uri =  artist_search['playlists']['items'][0]['uri']
    #this is the uri that we will search on
    tracks_new = get_playlist_tracks_uri(result_uri)
    create_dict(tracks_new)
    return()


#takes a username + uri
#this does not trigger the rest of the program.
#setting new global paramters
'''takes as input a string, and creates the format for a spotipy request'''
def Spotify_user_entry(user_name):
    #this is my friend danny who has several public playlists.
    input = user_name
    global total_string
    total_string = 'spotify:user:'
    total_string += input
    lp = spotipy.Spotify(auth=token)
    user_search = lp.user_playlists(input)
    #this is where we combine our data.
    list_to_keep = []
    list_of_names = []
    for i in range(len(user_search)):
        list_to_keep.append(user_search['items'][i]['uri'])
        list_of_names.append(user_search['items'][i]['name'])
        
    #list_to_keep will enable us to query to the function get_playlist_tracks
    #list_of_names will be the names of the playlist they choose to add.
    #Each of the two lists will be indexed the same so if the user chooses to add playlist 4, then
    #the list_to_keep will send index 4 in its list to gather those songs.
    
    #for testing we are just going to take the first query.
    #output = list_to_keep[0]
    #print(output)
    #user_public_tracks = get_playlist_tracks('dfox005',output)
    #create_dict(user_public_tracks)
    #return()
    global new_dict
    new_dict = {}
    for i in range(len(list_of_names)):
        new_dict[list_of_names[i]] = list_to_keep[i]
    global tester
    tester = new_dict.keys()
    print(new_dict)
    message = 'Spotify user playlists found!'
    flash(message, category='success')
    #user_public_tracks = get_playlist_tracks('dfox005',output)
    #create_dict(user_public_tracks)
    return(tester)
    
        
'''This will have to take some JSON'''
def create_dict(A_JSON):
    if token:
        # Primary query for tracks in playlist
        #in tracks we have all the data that we could possibly want.
        song_information = {
            'name' : [],
            'album' : [],
            'artist' : [],
            'release_date' : [],
            'length' : [],
            'acousticness' : [],
            'danceability' : [],
            'energy' : [],
            'instrumentalness': [],
            'key' : [],
            'liveness' : [],
            'loudness' : [],
            'mode' : [],
            'popularity' : [],
            'speechiness': [],
            'tempo': [],
            'valence': [],
        }
        
        #we have all the songinformation that we need
        id = []
        
        for items in A_JSON:
            track = items['track']['id']
            id.append(track)
        
        # we are going to make many requests to get all the details in the dictionary above.
        
        for song_request in id:
            kp = spotipy.Spotify(auth=token)
            key = kp.track(song_request)
            name = key['name']
            song_information['name'] += [name]
            
            album = key['album']['name']
            song_information['album'] += [album]
            song = key['artists'][0]['name']
            song_information['artist'] += [song]
            pop = key['popularity']
            song_information['popularity'] += [pop]
            release = key['album']['release_date']
            song_information['release_date'] += [release]
            length = key['duration_ms']
            song_information['length'] += [length]
            #the dictionary is full with all the information not regarding audio features
            #incomplete
            
            
            
            lp = spotipy.Spotify(auth=token)
            audio = lp.audio_features(song_request)
            #
            
            acoustic = audio[0]['acousticness']
            song_information['acousticness'] += [acoustic]
            danceability = audio[0]['danceability']
            song_information['danceability'] += [danceability]
            energy = audio[0]['energy']
            song_information['energy'] += [energy]
            instrumentalness = audio[0]['instrumentalness']
            song_information['instrumentalness'] += [instrumentalness]
            keys = audio[0]['key']
            song_information['key'] += [keys]
            liveness = audio[0]['liveness']
            song_information['liveness'] += [liveness]
            speech = audio[0]['speechiness']
            song_information['speechiness'] += [speech]
            tempo = audio[0]['tempo']
            song_information['tempo'] += [tempo]
            valence = audio[0]['valence']
            song_information['valence'] += [valence]
            mode = audio[0]['mode']
            song_information['mode'] += [mode]
            loud = audio[0]['loudness']
            song_information['loudness'] += [loud]
            
    return(print_csv(song_information))

'''paint the csv file to get each of the song informations.'''
def print_csv(song_information):
    for i in range(len(song_information['name'])):
        name = song_information['name'][i]
        album = song_information['album'][i]
        artist = song_information['artist'][i]
        release_date = song_information['release_date'][i]
        length = song_information['length'][i]
        acousticness = song_information['acousticness'][i]
        danceability = song_information['danceability'][i]
        energy = song_information['energy'][i]
        instrumentalness = song_information['instrumentalness'][i]
        key = song_information['key'][i]
        liveness = song_information['liveness'][i]
        loudness = song_information['loudness'][i]
        mode = song_information['mode'][i]
        popularity = song_information['popularity'][i]
        speechiness = song_information['speechiness'][i]
        tempo = song_information['tempo'][i]
        valence = song_information['valence'][i]

        check = Songs.query.filter_by(name = name, album = album, artist = artist).all()
        
        print(check)
        if len(check) == 0:
            add_song = Songs(name = name, album = album, artist = artist, release_date = release_date, length = length, acousticness = acousticness, danceability = danceability, energy = energy, instrumentalness = instrumentalness, key = key, liveness = liveness, loudness = loudness, mode = mode, popularity = popularity, speechiness = speechiness, tempo = tempo, valence = valence)
            db.session.add(add_song)
            db.session.commit()

        if likeSongs:
            likePPlay(name, album, artist)

def likePPlay(name, album, artist):
    check = Songs.query.filter_by(name = name, album = album, artist = artist).all()
    checkLike = Playlist.query.filter_by(song_id = check[0].id, user_id = current_user.id).all()
    if len(checkLike) == 0:
        add_liked = Playlist(user_id = current_user.id, song_id = check[0].id, likeability = 1)
        db.session.add(add_liked)
        db.session.commit()



@pplay.route('/', methods=['GET', 'POST'])
def index():
    user_name = request.args.get('user_name')
    playlist_name = request.form.get('addPlaylist')
    like_playlist = request.form.get('likePlaylist')
    global likeSongs
    likeSongs = False
    print(playlist_name)
    if user_name is not None:
        if len(user_name) > 0 and playlist_name is None:
            Spotify_user_entry(user_name)
        else:
            print('error')
    if playlist_name is not None:
        print(new_dict[playlist_name])
        print(total_string)
        get_playlist_tracks(total_string ,new_dict[playlist_name])
    if like_playlist is not None:
        likeSongs = True
        get_playlist_tracks(total_string ,new_dict[like_playlist])
        title = str(like_playlist)
        message = 'Added Songs in Playlist ' + title + ' to Liked Songs'
        flash(message, category='success')




    return render_template('pplay.html',  tester = tester , user=current_user)
