from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from db_link import get_liste_questionnaire, get_questions, add_question, add_answer, get_liste_id_nom_questionnaire,del_question
from werkzeug.utils import secure_filename
import requests
import os

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'xml'}

app = Flask(__name__)

app.config['SECRET_KEY']  = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
app.config['UPLOAD_FOLDER'] = 'static/uploaded_files'


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
            listid = []
            for i in range(len(que)):
                listid.append(que[i]['idq'])

    else:
        idqq = ''
        que = []
        listid = []

    return render_template("questionnaire.html", idqq = idqq, questions = que, lenque = len(que), listid = listid)

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


class uploadFileForm(FlaskForm):
    file = FileField('Fichier à importer')
    submit = SubmitField('Submit')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            return "file uploaded successfully"
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
    # dict_xml = get_dict_from_DB(idQ)
    # writter("test1.xml", "link_front_back/static/out/", dict_xml, True)
    return send_file("static/out/test1.xml", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)