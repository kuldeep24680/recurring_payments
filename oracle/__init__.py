import pymongo
from flask import Flask, redirect, session, render_template, g
from flask_mongoengine import MongoEngine
from celery import Celery

from oracle.local_config import MONGODB_SETTINGS, CELERY_SETTINGS, AWS_SETTINGS

mainapp = Flask(__name__)

db = MongoEngine(mainapp)

mainapp.config["MONGODB_SETTINGS"] = MONGODB_SETTINGS
# updating settings.
mainapp.config.update(AWS_SETTINGS)
mainapp.config.update(CELERY_SETTINGS)

def get_pymongo_client():
    global pymongo_db
    if pymongo_db == None:
        pymongo_client = pymongo.MongoClient(MONGODB_SETTINGS["HOST"])
        pymongo_db = pymongo_client[MONGODB_SETTINGS["DB"]]
    return pymongo_db