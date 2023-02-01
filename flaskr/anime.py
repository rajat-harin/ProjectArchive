import functools
from flask_cors import cross_origin
from urllib.request import Request, urlopen  
import json
import datetime

import pymongo

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for, escape
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.utils import date2Season


bp = Blueprint('anime', __name__, url_prefix='/anime')

@bp.route('/', methods=('GET','POST'))
@cross_origin()
def index():
    season = date2Season(datetime.date.today())
    url = "https://api.myanimelist.net/v2/anime/season/{}/{}?limit=50".format(datetime.date.today().year,season)
    req = Request(url)
    req.add_header('X-MAL-CLIENT-ID', current_app.config['X_MAL_CLIENT_ID'])
    resp = urlopen(req).read()
    data = json.loads(resp)

    return render_template('anime/index.html', animeList = data["data"])

@bp.route('/<id>', methods=('GET','POST'))
@cross_origin()
def getAnime(id):

    season = date2Season(datetime.date.today())
    fieldList = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"
    url = "https://api.myanimelist.net/v2/anime/{}?fields={}".format(escape(id),fieldList)
    req = Request(url)
    req.add_header('X-MAL-CLIENT-ID', current_app.config['X_MAL_CLIENT_ID'])
    resp = urlopen(req).read()
    data = json.loads(resp)

    return render_template('anime/anime.html', anime = data)