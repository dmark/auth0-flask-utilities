from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class NewUserForm(FlaskForm):
    given_name = StringField('Given Name', validators=[DataRequired()])
    family_name = StringField('Family Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Add')


class GetUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Get')


class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    email_verified = StringField('Email Verified', validators=[DataRequired()])
    updated = DateField('Last Updated', validators=[DataRequired()])
    user_id = StringField('Auth0 user_id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    created = StringField('Account Created Date', validators=[DataRequired()])
    user_metadata = TextAreaField('User Metadata', validators=[DataRequired()])
    app_metadata = TextAreaField('App Metadata', validators=[DataRequired()])
    last_ip = StringField('Last IP Address', validators=[DataRequired()])
    last_login = StringField('Last Login', validators=[DataRequired()])
    logins_count = StringField('Total Logins', validators=[DataRequired()])
    blocked_for = StringField('Blocked IP Addresses', validators=[DataRequired()])
    guardian_authenticators = StringField('MFA', validators=[DataRequired()])

    submit = SubmitField('Submit')
