from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from db_link import get_liste_questionnaire, get_questions, add_question, add_answer,del_question
from werkzeug.utils import secure_filename
import requests
import os

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['xml'])

app = Flask(__name__)

app.config['SECRET_KEY']  = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


Bootstrap(app)



class QuestionForm(FlaskForm):
        titre = StringField('Titre', validators=[DataRequired()])
        Typeq = SelectField('Type de question', choices=[('1', 'QCM'),('2', 'Réponse courte'),('3', 'Réponse longue')], validators=[DataRequired()])
        points = IntegerField('Points', validators=[DataRequired()])
        valeurpn = IntegerField('Valeur des points négatifs')
        submit = SubmitField('Submit')

class ReponseForm(FlaskForm):
        reponse = StringField('Réponse', validators=[DataRequired()])
        fraction = IntegerField('Fraction', validators=[DataRequired()])
        submit = SubmitField('Submit')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route("/") # page de base du site
def home():
    return render_template("home.html")

@app.route("/ajout/<idq>", methods =("GET","POST" ,))
def ajoutq(idq):
    form = QuestionForm()
    if form.valeurpn.data == None:
        form.valeurpn.data = 0
    if form.validate_on_submit():
        add_question(form.titre.data, idq, form.Typeq.data, 0, form.points.data, "", form.valeurpn.data)
        return redirect(url_for('ajoutr', idq=(get_questions(idq)[len(get_questions(idq))-1]['idq'])))
    return render_template("test.html", form=form)

@app.route("/ajout/<idq>/", methods =("GET","POST" ,))
def ajoutr(idq):
    form = ReponseForm()
    if form.validate_on_submit():
        add_answer(form.reponse.data, form.fraction.data, idq)
        return redirect(url_for('questionnaire'))
    return render_template("ajoutreponse.html", form=form)
@app.route("/questionnaire", methods=["POST","GET"])
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

@app.route("/questionnaire/<idq>", methods=["POST","GET"])
def question(idq):
    del_question(idq)
    return redirect(url_for('questionnaire'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/connexion")
def connexion():
    return render_template("connexion.html")

@app.route("/historique")
def historique():
    return render_template("historique.html")




if __name__ == "__main__":
    app.run(debug=True)