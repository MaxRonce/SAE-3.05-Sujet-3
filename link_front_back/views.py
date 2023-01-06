from .app import app
from .db_link import get_questions, get_liste_questionnaire, get_user, add_question, add_answer, get_liste_id_nom_questionnaire, del_question
from .models import User
import db_link

from flask import render_template, request, redirect, session,  url_for, flash, send_file
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField
from wtforms.validators import DataRequired

from parser.DB_to_XML import get_dict_from_DB
from parser.XML_Writter import *
import parser.XML_parser as XML_parser
from werkzeug.utils import secure_filename

import os

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
@login_required()
def questionnaire():
    if request.method == "POST":
        idqq = request.form["idqq"]
        if idqq == '' or not idqq.isnumeric():
            que = []
        else:
            que = get_questions(int(idqq))
            listid = []
            for i in range(len(que)):
                listid.append(que[i]['idq'])

    else:
        idqq = ''
        que = []
        listid = []

    return render_template("questionnaire.html", idqq = idqq, questions = que, lenque = len(que), listid = listid)

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


@app.route("/questionnaire/<idq>", methods=["POST","GET"])
def question(idq):
    del_question(idq)
    return redirect(url_for('questionnaire'))

class uploadFileForm(FlaskForm):
    file = FileField('Fichier à importer')
    submit = SubmitField('Submit')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def to_raw(string):
    return r"{}".format(string)
@app.route('/import', methods=['GET', 'POST'])
def uploader_file():
    form = uploadFileForm()
    if form.validate_on_submit() and request.method == 'POST':
        file = form.file.data
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

            #parse the file
            #get the file path
            file_path = to_raw(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            parsed_file = XML_parser.parse(file_path)
            db_link.add_questionnaire(parsed_file)
            return "File uploaded successfully and added to the database"


    return render_template('import.html', form=form)

class DownloadForm(FlaskForm):
    liste = SelectField("Questionnaire", choices=get_liste_id_nom_questionnaire())
    submit = SubmitField('submit')

@app.route('/export', methods=['GET', 'POST'])
def downloader_file():
    form = DownloadForm()
    if not form.validate_on_submit():
        return render_template("export.html", form=form)
    return redirect(url_for("download_file", idQ=form.liste.data))

@app.route('/downloadfile/<idQ>')
def download_file(idQ):
    name = "Export" + idQ+ ".xml"
    print(name)
    writter(name, 'parser/out/', get_dict_from_DB(idQ), category=True)

    return send_file("parser/out/"+name, as_attachment=True)