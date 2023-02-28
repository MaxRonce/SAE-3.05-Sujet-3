from sqlalchemy import exc
from .app import app, ALLOWED_EXTENSIONS
from .db_link import *
from .models import User
from .forms import *

from flask import render_template, request, redirect, session, url_for, flash, send_file, jsonify
from flask_login import login_user, current_user, logout_user, login_required

from link_front_back.parser.DB_to_XML import get_dict_from_DB
from link_front_back.parser.XML_Writter import *
import link_front_back.parser.XML_parser as XML_parser
from werkzeug.utils import secure_filename
import os


@app.route("/", methods=["POST", "GET"])  # page de base du site
def home():
    f = LoginForm()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            print(current_user)
            return redirect(url_for("home"))
    return render_template("home.html", form=f)


@app.route("/questionnaire", methods=["POST", "GET"])
@login_required
def questionnaire():

    # récupérer la liste de tous les questionnaires disponibles
    questionnaires = get_questionnaires()  # suppose que cette fonction récupère la liste des questionnaires depuis une source de données externe
    selected_idqq = -1
    if request.method == "POST":

        # récupérer l'ID du questionnaire sélectionné à partir de la liste déroulante
        selected_idqq = request.form["idqq"]
        if selected_idqq.isnumeric():
            # rediriger vers la page questionnaire avec l'ID sélectionné
            return render_template("questionnaire.html", idqq = int(selected_idqq), questionnaires=questionnaires,
                                   questions=get_questions(selected_idqq), nquest = get_questionnaire_name(selected_idqq))

    # si la méthode est GET, afficher la liste déroulante de tous les questionnaires
    return render_template("questionnaire.html", questionnaires=questionnaires, questions=get_questions(selected_idqq), idqq = selected_idqq)

@app.route("/questionnaire/<idq>", methods=["DELETE"])
def delete_question(idq):
    del_question(idq)
    return jsonify({"message": "Question deleted successfully."})

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


@app.route("/ajout/<idq>", methods=("GET", "POST",))
def ajoutq(idq):
    form = QuestionForm()
    if form.valeurpn.data == None:
        form.valeurpn.data = 0
    if form.validate_on_submit():
        add_question(form.titre.data, idq, form.Typeq.data, 0, form.points.data, "", form.valeurpn.data)
        return redirect(url_for('ajoutr', idq=(get_questions(idq)[len(get_questions(idq)) - 1]['idq'])))
    return render_template("test.html", form=form)


@app.route("/ajout/<idq>/", methods=("GET", "POST",))
def ajoutr(idq):
    form = ReponseForm()
    if form.validate_on_submit():
        add_answer(form.reponse.data, form.fraction.data, idq)
        return redirect(url_for('questionnaire'))
    return render_template("ajoutreponse.html", form=form)


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
            try:
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                       secure_filename(file.filename)))
                # get the file path
                file_path = to_raw(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                                secure_filename(file.filename)))
                parsed_file = XML_parser.parse(file_path)
                add_questionnaire(parsed_file)
                flash('File successfully uploaded')
            except ValueError as e:
                flash('Error: ' + str(e))
            except exc.SQLAlchemyError as e:
                flash('Error while uploading file')
                flash(str(e))

    return render_template('import.html', form=form)





@app.route('/export', methods=['GET', 'POST'])
def downloader_file():
    form = DownloadForm()
    if not form.validate_on_submit():
        return render_template("export.html", form=form)
    return redirect(url_for("download_file", idQ=form.liste.data))


@app.route('/downloadfile/<idQ>')
def download_file(idQ):
    name = "Export" + idQ + ".xml"
    print(name)
    writter(name, 'link_front_back/parser/out/', get_dict_from_DB(idQ), category=True)

    return send_file("parser/out/" + name, as_attachment=True)


@app.route('/choose')
def choose_qcm():
    return render_template("chooseqcm.html",questionnaires=get_questionnaires())

@app.route('/answer/<idq>')
def answer_qcm(idq):
    return render_template("answerqcm.html")