from flask import url_for, redirect, render_template, request, abort

import flask_admin
import flask_admin.contrib.sqla as flask_sql

from velican import app, db
from velican.models import blog

admin = flask_admin.Admin(app, 'Velikán',
    # base_template='my_master.html',
    template_mode='bootstrap4',
)
admin.add_view(flask_sql.ModelView(blog.Blog, db.session))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)