from flask_pymongo import PyMongo
from flask import current_app, g


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        cx = g._database = PyMongo(current_app).cx
        db = g._database = cx.get_database('ProjectArchive')

    return db


def close_db(e=None):
    db = g.pop('_database',None)

    if db is not None:
        db.close()