import pelican

from velican.app import app, db
from velican import models

from pathlib import Path

def _generate_blog(site: models.Site, live: bool, user: str):
    publish = models.Publish.current(preview=not live)
    if publish is not None:
        return "Publishing in progress"
    try:
        pelican_conf = site.as_settings()
        pelican_conf.update(
            output_dir=app.conf['SERVER_ROOT'] / "production" if live else "staging" / site.domain,
            content_dir=app.conf['SERVER_ROOT'] / "content" / site.domain,
        )
        proc = pelican.Pelican(pelican_conf)
        proc.run()
        publish.failed = False
    except Exception as e:
        publish.result = str(e)
        publish.failed = True
    db.session.add(publish)
    db.session.commit()

def on_post_save(instance: models.Post):
    with open(app.config['CONTENT_DIR'] / instance.category / instance.slug + ".md", "wt") as f:
        f.write(instance.content)

def on_page_save(instance: models.Page):
    with open(app.config['CONTENT_DIR'] / instance.category / instance.slug + ".md", "wt") as f:
        f.write(instance.content)

def on_create(instance: models.Site):
    Path(app.conf['OUTPUT_ROOT'] / instance.domain).mkdir(exist_ok=False)
    Path(app.conf['SOURCE_ROOT'] / instance.domain).mkdir(exist_ok=False)

def on_publish(instance: models.Publish):
    _generate_blog(instance.site, True, current_user())

def on_preview(instance: models.Publish):
    _generate_blog(instance.site, False, current_user())

def init():
    pass