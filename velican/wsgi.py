from .app import app, db
from . import views as _
from . import models as _

application = app

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()