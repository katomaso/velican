import pelican
from . import models
from flask import request, render_template, login_required
from flask_login import current_user, login_user
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from .app import app, db, social, published
from .models import OAuth
from . import controllers

facebook_blueprint = make_facebook_blueprint(
    client_id=app.config['FACEBOOK_ID'],
    client_secret=app.config['FACEBOOK_SECRET'],
    scope="email,public_profile,pages_manage_posts,pages_show_list"
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)

@app.route('/profile')
@login_required
def profile():
    return render_template(
        'profile.html',
        content='Profile Page',
        twitter_conn=social.twitter.get_connection(),
        facebook_conn=social.facebook.get_connection())

@app.route('/site/<site:path>/publish/', methods=['POST'])
def publish(site: str, user="admin"):
    if models.Publish.current():
        return "Publishing in progress"
    publish = models.Publish()
    try:
        published.send()
        publish.failed = False
    except Exception as e:
        publish.result = str(e)
        publish.failed = True
    db.session.add(publish)
    db.session.commit()

@app.route('/site/<site:path>/preview/', methods=['GET'])
def preview(site: str, user="admin"):
    """Get the publishing progress"""
    pass
