from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Songs
from .models import Playlist
from .models import User
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/')
def index():
    song = request.args.get('song')
    artists = Songs.query.filter_by(artist=song).all()
    songs = Songs.query.filter_by(name=song).all()
    albums = Songs.query.filter_by(album=song).all()
    return render_template('home.html', artists=artists, songs=songs, albums=albums, user=current_user)


@views.route('/', methods=['GET', 'POST'])
@ login_required
def likeSongs():
    var = request.form.get('reaction')
    like = var.find('like')
    print(like)
    value = int(var.replace('dis','').replace('like',''))
    qs = Songs.query.get_or_404(value)
    # x = Playlist(user_id=current_user.id, likeability=0)
    if request.method == 'POST':
        print("test1")
        try:
            if like == 0:
                add_track = Playlist(user_id=current_user.id, likeability=1, song_id=qs.id )
            #new_playlist = Playlist(data=playlist, user_id=current_user.id)
            else:
                add_track = Playlist(user_id=current_user.id, likeability=0, song_id=qs.id )
            #db.session.add(new_playlist)
            #db.session.commit()
            db.session.add(add_track)
            # db.session.add(qs)
            #print(add_track.id)
            db.session.commit()
            if like == 0:
                flash('Added to Liked Songs', category='success')
                
            else:
                flash('Added to Dislike Songs', category='error')

            return render_template('home.html',user=current_user)
            
        except:

            return "There was a problem adding to liked songs"
        # else:
            # return render_template('home.html')




@ views.route('/', methods=['GET', 'POST'])
@ login_required
def home():
    if request.method == 'POST':
        playlist = request.form.get('playlist')

        if len(playlist) < 1:
            flash('Playlist is too short!', category='error')
        else:
            new_playlist = Playlist(data=playlist, user_id=current_user.id)
            db.session.add(new_playlist)
            db.session.commit()
            flash('Playlist added!', category='success')

    return render_template("home.html", user=current_user)


@ views.route('/delete-playlist', methods=['POST'])
def delete_playlist():
    playlist = json.loads(request.data)
    playlistId = playlist['playlistId']
    playlist = Playlist.query.get(playlistId)
    if playlist:
        if playlist.user_id == current_user.id:
            db.session.delete(playlist)
            db.session.commit()

    return jsonify({})
