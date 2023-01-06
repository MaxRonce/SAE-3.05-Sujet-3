from .app import app
from .db_link import get_questions, get_liste_questionnaire, get_user
from .models import User

from flask import render_template, request, redirect, session,  url_for
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField
from wtforms.validators import DataRequired

@app.route("/", methods=["POST", "GET"]) # page de base du site
def home():
    f = LoginForm()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            print(current_user)
            return redirect(url_for("home"))
    return render_template("home.html", form=f)

@app.route("/questionnaire", methods=["POST","GET"])
@login_required
def questionnaire():
    if request.method == "POST":
        idqq = request.form["idqq"]
        if idqq == '' or not idqq.isnumeric():
            que = []
        else:
            que = get_questions(int(idqq))
    else:
        idqq = ''
        que = []
    return render_template("questionnaire.html", idqq = idqq, questions = que, lenque = len(que))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profil")
@login_required
def profil():
    return render_template("profil.html")

@app.route("/logout", methods=["post"])
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/historique")
@login_required
def historique():
    return render_template("historique.html")

@app.route("/ajout")
@login_required
def ajout_question():
    return render_template("ajouter_question.html")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def get_authenticated_user(self):
        user = get_user(self.username.data)
        if user is None:
            return None
        from .models import User
        us = User(user.idUser, user.mdpUser)
        return us if self.password.data == us.password else None