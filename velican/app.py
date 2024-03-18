from flask import Flask
import flask_sqlalchemy as flask_sql
from flask.signals import Namespace

from . import settings

app = Flask(__name__)
# app.config.from_pyfile('config.cfg')
app.config.from_object(settings)

db = flask_sql.SQLAlchemy(app)

signals = Namespace("velikan")

saved = signals.signal('saved')
previewed = signals.signal('previewed')
published = signals.signal('published')