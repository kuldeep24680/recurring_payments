from flask import Flask, redirect, session, render_template, g
from flask_mongoengine import MongoEngine
from oracle.job import make_celery

mainapp = Flask(__name__)
db = MongoEngine(mainapp)

celery = make_celery(
    "oracle.tasks",
    mainapp.config["CELERY_broker_url"],
    mainapp.config["CELERY_result_backend"],
)
celery.autodiscover_tasks(["oracle"])