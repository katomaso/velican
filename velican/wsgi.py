from velican.app import app, db

from velican import admin as _
from velican import views as _
from velican import models as _

application = app

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()