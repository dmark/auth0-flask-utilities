from flask import Flask
from flask import request
from flask import render_template


from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NewUserForm(FlaskForm):
    given_name = StringField('Given Name', validators=[DataRequired()])
    family_name = StringField('Family Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Add')


class GetUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Get')


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app


app = create_app()
app.config['SECRET_KEY'] = '03e930e7090ea7f0096881067415f9f7'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def user(name):
    return render_template('user.html')


@app.route('/user/add', methods=['GET', 'POST'])
def user_add():
    form = NewUserForm()
    return render_template('adduser.html', form=form)


@app.route('/user/get', methods=['GET', 'POST'])
def user_get():
    form = GetUserForm()
    return render_template('getuser.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
