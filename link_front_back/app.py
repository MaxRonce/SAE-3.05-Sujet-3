from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from db_link import get_liste_questionnaire, get_questions, add_question

app = Flask(__name__)

app.config['SECRET_KEY']  = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

Bootstrap(app)


class QuestionForm(FlaskForm):
        titre = StringField('Titre', validators=[DataRequired()])
        Nbrep = IntegerField('Nombre de réponses', validators=[DataRequired()])
        Typeq = SelectField('Type de question', choices=[('11', 'QCM'),('12', 'Réponse courte'),('13', 'Réponse longue')], validators=[DataRequired()])
        submit = SubmitField('Submit')


@app.route("/") # page de base du site
def aff_home():
    return render_template("home.html")

@app.route("/ajout2", methods=['GET', 'POST'])
def aff_ajoutq():
    form = QuestionForm()
    if form.validate_on_submit():
        add_question(form.titre.data, 1, form.Typeq.data)
        return redirect(url_for('aff_home'))
    return render_template("test.html", form=form)


@app.route("/questionnaire", methods=["POST","GET"])
def aff_questionnaire():
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
def aff_about():
    return render_template("about.html")

@app.route("/connexion")
def aff_connexion():
    return render_template("connexion.html")

@app.route("/historique")
def aff_historique():
    return render_template("historique.html")

@app.route("/ajout")
def aff_ajout_question():
    return render_template("ajouter_question.html")

if __name__ == "__main__":
    app.run(debug=True)