import pymongo
from flask import Flask, redirect, session, render_template, g
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from celery import Celery

from oracle.settings import MONGODB_SETTINGS, CELERY_SETTINGS, AWS_SETTINGS

mainapp = Flask(__name__)

db = MongoEngine(mainapp)

mainapp.config["MONGODB_SETTINGS"] = MONGODB_SETTINGS
# updating settings.
mainapp.config.update(AWS_SETTINGS)
mainapp.config.update(CELERY_SETTINGS)
mainapp.config["SECRET_KEY"] = "^udtr!d^_vw22_+a=f1*au01xn(adtyce7^5k5ndkf6e%2z%aq"

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.needs_refresh_message = (
    u"To protect your account, please re-authenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"
login_manager.init_app(mainapp)

@login_manager.user_loader
def load_user(userid):
    from organisation.model import OracleOrgUser

    return OracleOrgUser.objects(id=userid).first()

from dashboard.views import auth_views
mainapp.register_blueprint(auth_views)

def get_pymongo_client():
    global pymongo_db
    if pymongo_db == None:
        pymongo_client = pymongo.MongoClient(MONGODB_SETTINGS["HOST"])
        pymongo_db = pymongo_client[MONGODB_SETTINGS["DB"]]
    return pymongo_db