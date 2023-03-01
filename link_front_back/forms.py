from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired

from .db_link import get_liste_id_nom_questionnaire, get_user
from .models import User
from hashlib import sha256


class DownloadForm(FlaskForm):
    def __init__(self, idu):
        super().__init__()
        self.liste.choices = get_liste_id_nom_questionnaire(idu)

    liste = SelectField("Questionnaire")
    submit = SubmitField('submit')


class uploadFileForm(FlaskForm):
    file = FileField('Fichier à importer')
    submit = SubmitField('Submit')


class QuestionForm(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired()])
    Typeq = SelectField('Type de question', choices=[('1', 'QCM'), ('2', 'Réponse courte'), ('3', 'Réponse longue')],
                        validators=[DataRequired()])
    points = IntegerField('Points', validators=[DataRequired()])
    valeurpn = IntegerField('Valeur des points négatifs')
    submit = SubmitField('Submit')


class ReponseForm(FlaskForm):
    reponse = StringField('Réponse', validators=[DataRequired()])
    fraction = IntegerField('Fraction', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def get_authenticated_user(self):
        user = get_user(self.username.data)
        if user is None:
            return None
        us = User(user.idUser, user.mdpUser)
        salted_input = self.username.data + self.password.data
        salted_input = sha256(salted_input.encode('utf-8')).hexdigest()
        return us if salted_input == us.password else None
