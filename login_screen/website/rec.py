from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Songs
from .models import Playlist
from .models import User
from .models import recommendedSongs
from . import db
import json

rec = Blueprint('rec', __name__)

def smartAlgo():
    delete_old = recommendedSongs.query.filter_by(user_id = current_user.id).all()
    for old in delete_old:
        db.session.delete(old)
    db.session.commit()

    traits = ['acousticness','danceability','energy','instrumentalness','liveness','loudness','popularity','speechiness','tempo','valence']
    likedUserSongs = Playlist.query.filter_by(user_id = current_user.id, likeability = 1).all()
    dislikedUserSongs = Playlist.query.filter_by(user_id = current_user.id, likeability = 0).all()
    if len(likedUserSongs) != 0 and len(dislikedUserSongs) != 0:
        likedSongs = []
        dislikedSongs = []
        for x in likedUserSongs:
            likedSongs.append(Songs.query.filter_by(id = x.song_id).all()[0])
        for y in dislikedUserSongs:
            dislikedSongs.append(Songs.query.filter_by(id = x.song_id).all()[0])
        queryText = 'Select * From songs Where '
        likedTraits = []
        dislikedTraits = []
        first = True
        for trait in traits:
            count = 0
            liked = 0.0
            disliked = 0.0
            for songs in likedSongs:
                liked += vars(songs)[trait]
                count += 1
            liked = float(liked/count)
            likedTraits.append(liked)
            count = 0
            for songs in dislikedSongs:
                disliked += vars(songs)[trait]
                count += 1
            disliked = float(disliked/count)
            dislikedTraits.append(disliked)

            if abs(liked - disliked) > 0.1:
                if not first:
                    queryText = queryText + 'and '
                median = (liked + disliked) / 2
                if liked > disliked: # liked is higher
                    queryText = queryText + trait + ' > ' + str(median) + ' '
                    first = False
                else:
                    queryText = queryText + trait + ' < ' + str(median) + ' '
                    first = False

        if not first: # prevents a person with no analytices from being run
            test = 'Select  * From songs Where acousticness > 0.5 and energy < 0.8'
            recommend = db.session.execute(queryText)
            counter = 0
            for i in recommend:
                check_recommended = Playlist.query.filter_by(user_id=current_user.id, song_id = i[0]).all()
                if len(check_recommended) == 0:
                    add_recommended = recommendedSongs(user_id=current_user.id, song_id = i[0])
                    db.session.add(add_recommended)
                    counter += 1
                
                if counter >= 10:
                    db.session.commit()
                    return()
            db.session.commit()




@rec.route('/', methods=['GET', 'POST'])
def index():
    #song = request.args.get('song')
    var = request.form.get('rereaction')
    if var is not None:
        like = var.find('like')
        value = int(var.replace('dis','').replace('like',''))
        qs = Songs.query.get_or_404(value)
        if like == 0:
            add_track = Playlist(user_id=current_user.id, likeability=1, song_id=qs.id )
            title = qs.name
            message = title + ' Added to Liked Songs'
            flash(message, category='success')
        else:
            add_track = Playlist(user_id=current_user.id, likeability=0, song_id=qs.id )
            title = qs.name
            message = title + ' Added to Disliked Songs'
            flash(message, category='error')
        db.session.add(add_track)
        db.session.commit()

    smartAlgo()
    userSongs = recommendedSongs.query.filter_by(user_id = current_user.id).all()
    global songs
    songs = []
    print(userSongs)
    for x in userSongs:
        print (x.song_id)
        #var = Songs.query.filter_by(id = x.song_id).all()
        #print(var)
        songs.append(Songs.query.filter_by(id = x.song_id).all()[0])
    print(songs)
    #for y in songs:
        #print(y.name)

    return render_template('rec.html', songs=songs , user=current_user)



# @rec.route('/', methods=['GET', 'POST'])
# @ login_required
# def likeSongs():
#     var = request.form.get('rereaction')
#     like = var.find('like')
#     print(like)
#     value = int(var.replace('dis','').replace('like',''))
#     qs = Songs.query.get_or_404(value)
#     # x = Playlist(user_id=current_user.id, likeability=0)
#     if request.method == 'POST':
#         print("test1")
#         try:
#             if like == 0:
#                 add_track = Playlist(user_id=current_user.id, likeability=1, song_id=qs.id )
#             #new_playlist = Playlist(data=playlist, user_id=current_user.id)
#             else:
#                 add_track = Playlist(user_id=current_user.id, likeability=0, song_id=qs.id )
#             #db.session.add(new_playlist)
#             #db.session.commit()
#             db.session.add(add_track)
#             # db.session.add(qs)
#             #print(add_track.id)
#             db.session.commit()
#             if like == 0:
#                 flash('Added to Liked Songs', category='success')
                
#             else:
#                 flash('Added to Dislike Songs', category='error')

#             return render_template('rec.html',user=current_user)
            
#         except:

#             return "There was a problem adding to liked songs"
#         # else:
#             # return render_template('home.html')