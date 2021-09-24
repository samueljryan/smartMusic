from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))
    likeability = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    playlists = db.relationship('Playlist')

class userPlaylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    playlist_name = db.Column(db.String(150))

class recommendedSongs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))

class Songs(db.Model):
    #__searchable__ = ['name','album','artist']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    album = db.Column(db.String(150))
    artist = db.Column(db.String(150))
    release_date = db.Column(db.String(150))
    length = db.Column(db.Integer)
    acousticness = db.Column(db.Integer)
    danceability = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    instrumentalness = db.Column(db.Integer)
    key = db.Column(db.Integer)
    liveness = db.Column(db.Integer)
    loudness = db.Column(db.Integer)
    mode = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    speechiness = db.Column(db.Integer)
    tempo = db.Column(db.Integer)
    valence = db.Column(db.Integer)
