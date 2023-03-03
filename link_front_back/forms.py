from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FileField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, regexp

from .db_link import get_liste_id_nom_questionnaire, get_user, add_user
from .models import User
from hashlib import sha256

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

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
    Typeq = SelectField('Type de question', choices=[('1','Réponse courte'),('2','Vrai/Faux'),('3', 'QCM')],
                        validators=[DataRequired()])
    points = IntegerField('Points', validators=[DataRequired()])
    valeurpn = IntegerField('Valeur des points négatifs')
    submit = SubmitField('Submit')

class EquestionForm(FlaskForm):
    WTF_CSRF_ENABLED = False

    titre = StringField('Titre')
    Typeq = SelectField('Type de question', choices=[('1','Réponse courte'),('2','Vrai/Faux'),('3', 'QCM')],
                        validators=[DataRequired()])
    points = IntegerField('Points')
    valeurpn = IntegerField('Valeur des points négatifs')
    submit = SubmitField('Submit')

class QCMform(FlaskForm):
    reponse1 = StringField('Réponse', validators=[DataRequired()])
    reponse2 = StringField('Réponse')
    reponse3 = StringField('Réponse')
    reponse4 = StringField('Réponse')
    fraction1 = StringField('Fraction', validators=[DataRequired()])
    fraction2 = StringField('Fraction')
    fraction3 = StringField('Fraction')
    fraction4 = StringField('Fraction')
    submit = SubmitField('Submit')

class TrueFalseForm(FlaskForm):
    true_false = MultiCheckboxField('Label', choices=[('1', 'True'), ('2', 'False')])
    submit = SubmitField('Submit')

class ReponseCourteForm(FlaskForm):
    reponse1 = StringField('Réponse', validators=[DataRequired()])
    fraction1 = StringField('Fraction', validators=[DataRequired()])
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


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def new_user(self):
        salted_input = self.username.data + self.password.data
        salted_input = sha256(salted_input.encode('utf-8')).hexdigest()
        add_user(self.username.data, salted_input)
        return True
