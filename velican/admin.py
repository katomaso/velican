import flask_admin
import flask_admin.contrib.sqla as flask_sql

from velican import models
from velican.app import app, db

admin = flask_admin.Admin(app, 'Velikán',
    # base_template='my_master.html',
    template_mode='bootstrap4',
)

admin.add_view(flask_sql.ModelView(models.Site, db.session))
admin.add_view(flask_sql.ModelView(models.Post, db.session))
admin.add_view(flask_sql.ModelView(models.Page, db.session))
admin.add_view(flask_sql.ModelView(models.Category, db.session))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)