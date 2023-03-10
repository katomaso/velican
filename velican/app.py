from flask import Flask
import flask_sqlalchemy as flask_sql
import flask_social
from flask.signals import Namespace

from . import settings

app = Flask(__name__)
# app.config.from_pyfile('config.cfg')
app.config.from_object(settings)

db = flask_sql.SQLAlchemy(app)

social = flask_social.core.Social(app=app, datastore=db)

signals = Namespace("velikan")

saved = signals.signal('saved')
previewed = signals.signal('previewed')
published = signals.signal('published')