import json
import datetime
from pathlib import Path
from velican import db  # flask_sqlalchemy instance

themes = {
    "default": {"value": "default", "label": "default", "selected": False},
}

languages = {
    "cs_CZ": {"value": "cs_CZ", "label": "Česky", "selected": False},
    "en_US": {"value": "en_US", "label": "English", "selected": False},
}


class User(db.Model):
    nick
    domain


class Permission(db.Model):
    user
    model
    action (choice=("create", "edit", "view"))


#?? class Theme
#??   properties...

class Blog(db.Model):
    owner = db.Column(db.String(64), primary_key=True)
    domain = db.Column(db.String(32), primary_key=True, default="example.com")
    theme = db.Column(db.String(32), default="default")
    lang = db.Column(db.String(48), default="cs_CZ")
    timezone = db.Column(db.String(128), default="Europe/Prague")
    title = db.Column(db.String(128), default="")
    subtitle = db.Column(db.String(128), default="")
    twitter = db.Column(db.String(128), default="")
    linkedin = db.Column(db.String(128), default="")
    github = db.Column(db.String(128), default="")

    @classmethod
    def list_domains():
        """Caddy helper function about managed domains"""
        return json.dumps(Blog.all().map(lambda b: b.domain).collect())

    def as_settings(self):
        return {
            "output_dir": paths['OUTPUT'] / self.domain,
            "content_dir": paths['SOURCE'] / self.domain,
        }


class Theme(db.Model):
    pass


class Publish(db.Model):
    blog = db.Column(db.String(32))
    user = db.Column(db.String(64))
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    result = db.Column(db.String(512))
    failed = db.Column(db.Boolean(), nullable=True)

    def save(self, created):
        if created:
            self.__publish()
        super().save(created=created, **kwargs)

    def __publish(self):
        if proc_lock:
            raise PublishInProgress()
        try:
            proc = pelican.Pelican(blog.as_settings())
            proc.run()
            self.failed = False
        except Exception as e:
            self.result = str(e)
            self.failed = True


class Post(db.Model):
    blog = db.Column()
    creator = db.Column()
    title = db.Column()
    slug = db.Column()
    categories = db.Column()
    author = db.Column()
    lang = db.Column()
    description = db.Column()
    content = db.Column()
    public = db.Column(db.Boolean(), default=True)
    # one can "open" and "close" the post so more people don't edit it at once
    _opened = db.Column(db.DateTime(nullable=True))
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    updated = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    def save(self, **kwargs):
        with open(self.blog.content_dir / self.slug + ".md", "wt") as f:
            f.write(self.content)
        super().save(self, **kwargs)


class Category(db.Model):
    blog = db.Column()
    name = db.Column()


# @app.route('/domain', methods=['GET'])
# def domain_get():
#     user = request

# @app.route('/domain', methods=['POST', 'GET'])
# def domain_post():
#     domain = request.form.get('domain')
#     themes.get[request.form.get('theme')]["selected"] = True
#     lang = request.form.get('lang')
#     timezone = request.form.get('timezone')
#     title = request.form.get('title')
#     subtitle = request.form.get('subtitle')
#     twitter = request.form.get('twitter')
#     linkedin = request.form.get('linkedin')
#     github = request.form.get('github')
