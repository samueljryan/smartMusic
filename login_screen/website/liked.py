from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Songs
from .models import Playlist
from .models import User
from . import db
import json


liked = Blueprint('liked', __name__)


@liked.route('/', methods=['GET', 'POST'])
def index():
    like = request.form.get('like')
    dislike = request.form.get('dislike')
    delete = request.form.get('delete')
    print(like)
    print(dislike)
    print(delete)

    if like is not None:
        songToUpdate = Playlist.query.filter_by(user_id = current_user.id, song_id = like).all()[0]
        songToUpdate.likeability = 1
        db.session.commit()
        title = Songs.query.filter_by(id = like).all()[0].name
        message = title + ' Added to Liked Songs'
        flash(message, category='success')
    
    if dislike is not None:
        songToUpdate = Playlist.query.filter_by(user_id = current_user.id, song_id = dislike).all()[0]
        songToUpdate.likeability = 0
        db.session.commit()
        title = Songs.query.filter_by(id = dislike).all()[0].name
        message = title + ' Added to Disiked Songs'
        flash(message, category='error')

    if delete is not None:
        songToUpdate = Playlist.query.filter_by(user_id = current_user.id, song_id = delete).all()[0]
        db.session.delete(songToUpdate)
        db.session.commit()
        title = Songs.query.filter_by(id = delete).all()[0].name
        message = title + ' Deleted from Liked Songs'
        flash(message, category='error')

    userSongs = Playlist.query.filter_by(user_id = current_user.id)
    likedSongs = []
    dislikedSongs = []
    for i in userSongs:
        if i.likeability == 1:
            likedSongs.append(Songs.query.filter_by(id = i.song_id).all()[0])
        else:
            dislikedSongs.append(Songs.query.filter_by(id = i.song_id).all()[0])
    return render_template('liked.html', user = current_user, liked=likedSongs, disliked=dislikedSongs)