import json

from datetime import datetime, timedelta
from flask_login import UserMixin, OAuthConsumerMixin, LoginManager, current_user
from velican.app import app, db

themes = {
    "default": {"value": "default", "label": "default", "selected": False},
}

languages = {
    "cs_CZ": {"value": "cs_CZ", "label": "Česky", "selected": False},
    "en_US": {"value": "en_US", "label": "English", "selected": False},
}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)


#?? class Theme
#??   properties...

class Site(db.Model):
    domain = db.Column(db.String(32, primary_key=True, default="example.com"))
    # owner = db.Column(db.String(64, default="admin"))
    theme_name = db.Column(db.String(32, default="default"))
    lang = db.Column(db.String(48, default="cs_CZ"))
    timezone = db.Column(db.String(128, default="Europe/Prague"))
    title = db.Column(db.String(128, nullable=True))
    subtitle = db.Column(db.String(128, nullable=True))
    twitter = db.Column(db.String(128, nullable=True))
    linkedin = db.Column(db.String(128, nullable=True))
    github = db.Column(db.String(128, nullable=True))

    @classmethod
    def list_domains():
        """Caddy helper function about managed domains"""
        return json.dumps(Site.all().map(lambda b: b.domain).collect())

class User(db.Model):
    nick = db.Column(db.String(64, primary_key=True))
    site_id =  db.Column(db.String(32, primary_key=True))


class Theme(db.Model):
    name = db.Column(db.String(32, primary_key=True))

class Category(db.Model):
    site_id = db.Column(db.String(32, primary_key=True))
    name = db.Column(db.String(32, primary_key=True))

class Publish(db.Model):
    site_id = db.Column(db.String(32, primary_key=True))
    user = db.Column(db.String(64, default="admin", primary_key=True))
    preview = db.Column(db.String(False))
    started = db.Column(db.DateTime(default=datetime.utcnow, primary_key=True))
    finished = db.Column(db.DateTime(onupdate=datetime.utcnow))
    result = db.Column(db.String(512))
    failed =  db.Column(db.Bool(default=False))

    @classmethod
    def current(site: str, preview=False):  # return instance of itself
        return Publish.query.filter_by(
        Publish.site==site,
        Publish.user==current_user(),
        Publish.preview==preview,
        Publish.started > datetime.utcnow()-timedelta(minute=1),
        Publish.finished is None).get()


class Post(db.Model):
    site_id = db.Column(db.String(32, primary_key=True))
    creator = db.Column(db.String(64, default="admin"))
    title = db.Column(db.String(128))
    slug = db.Column(db.String(64, primary_key=True))
    category_id = db.Column(db.String(32))
    author = db.Column(db.String(32))
    lang = db.Column(db.String(2))
    description = db.Column(db.Text())
    content = db.Column(db.Text())
    draft = db.Column(db.String(True))
    # one can "open" and "close" the post so more people don't edit it at once
    _opened = db.Column(db.DateTime(nullable=True))
    created = db.Column(db.DateTime(default=datetime.utcnow))
    updated = db.Column(db.DateTime(onupdate=datetime.utcnow))


class Page(db.Model):
    site_id = db.Column(db.String(32, primary_key=True))
    slug = db.Column(db.String(64, primary_key=True))
    title = db.Column(db.String(128))
    content = db.Column(db.Text())
    # one can "open" and "close" the post so more people don't edit it at once
    _opened = db.Column(db.DateTime(nullable=True))
    created = db.Column(db.DateTime(default=datetime.utcnow))
    updated = db.Column(db.DateTime(onupdate=datetime.utcnow))

    def save(self, **kwargs):
        with open(self.site.content_dir / self.slug + ".md", "wt") as f:
            f.write(self.content)
        super().save(self, **kwargs)
