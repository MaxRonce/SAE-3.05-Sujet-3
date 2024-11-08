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
    rf = RegisterForm()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    if rf.validate_on_submit():
        try:
            rf.new_user()
            flash("User registered successfully.")
        except exc.IntegrityError:
            flash("User already exists.")
    return render_template("home.html", form=f, form2=rf, login="HIDE", register="HIDE")

@app.route("/questionnaire", methods=["POST", "GET"])
@login_required
def questionnaire():

    # User is authenticated, proceed with the questionnaire logic
    idu = current_user.username
    questionnaires = get_liste_questionnaires(idu)
    selected_idqq = -1
    if request.method == "POST":
        selected_idqq = request.form.get("idqq")
        if selected_idqq and selected_idqq.isnumeric():
            return render_template("questionnaire.html", idqq=int(selected_idqq), questionnaires=questionnaires,
                                   questions=get_questions(selected_idqq), nquest=get_questionnaire_name(selected_idqq))
    return render_template("questionnaire.html", questionnaires=questionnaires, questions=get_questions(selected_idqq), idqq=selected_idqq)

@app.errorhandler(401)
def unauthorized(e):
    f = LoginForm()
    rf = RegisterForm()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            print(current_user)
            return redirect(url_for("home"))
    if rf.validate_on_submit():
        try:
            rf.new_user()
            flash("User registered successfully.")
        except exc.IntegrityError:
            flash("User already exists.")
    return render_template("home.html", form=f, form2=rf, login="SHOW", register="HIDE")

@app.route("/questionnaire/<idq>", methods=["DELETE"])
def delete_question(idq):
    del_question(idq)
    return jsonify({"message": "Question deleted successfully."})


@app.route("/questionnaires", methods=["POST", "GET"])
@login_required
def questionnaires():
    idu = current_user.username
    return render_template("listquestionnaire.html", questionnaires = get_liste_questionnaires(idu))



@app.route("/questionnaires/<idq>", methods=["DELETE"])
def delete_questionnaire(idq):
    del_questionnaire(idq)
    return jsonify({"message": "Questionnaire deleted successfully."})
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
@app.route("/editquestion/<idq>", methods=["GET", "POST"])
def edit_question(idq):
    form = EquestionForm()
    form.Typeq.default = get_question(idq)['idt']
    form.process(request.form)
    if form.validate():
        print("valid")
    if form.is_submitted():
        print("submitted")
    print(form.errors)
    if form.validate_on_submit():
        modifq(form.titre.data, idq, form.Typeq.data, 0, form.points.data, "",form.valeurpn.data)
        return redirect(url_for('questionnaire'))
    return render_template("editquestion.html", form=form, question = get_question(idq))

@app.route("/addquestionnaire", methods=["GET", "POST"])
def add_questionnairepage():
    form = QuestionnaireForm()
    if form.validate_on_submit():
        add_questionnaire2(form.nom.data, form.info.data, current_user.username)
        return redirect(url_for('questionnaire'))
    return render_template("addquestionnaire.html", form=form)
@app.route("/ajout/<idq>/", methods=("POST", "GET"))
def ajoutr(idq):
    form = None
    match get_question(idq)['idt']:
        case 1:
            form = ReponseCourteForm()
        case 2:
            form = TrueFalseForm()
        case 3:
            form = QCMform()
    if form.validate_on_submit():
        print(get_question(idq)['idt'])
        match get_question(idq)['idt']:
            case 1:
                add_answer(form.reponse1.data, form.fraction1.data, idq)
                return redirect(url_for('questionnaire'))
            case 2:
                option = request.form['options']
                print(option)
                add_answer(option, 100, idq)
                if option == "true":
                    add_answer("false", 0, idq)
                else:
                    add_answer("true", 0, idq)
                return redirect(url_for('questionnaire'))
            case 3:
                for i in range(4):
                    m = "reponse" + str(i + 1)
                    n = "fraction" + str(i + 1)
                    op = getattr(form, m)
                    od = getattr(form, n)
                    add_answer(op.data, od.data, idq)
                    print(op.data)
                return redirect(url_for('questionnaire'))
        return redirect(url_for('questionnaire'))
    print(form.errors)
    return render_template("ajoutreponse.html", form=form, idt = get_question(idq)['idt'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def to_raw(string):
    return r"{}".format(string)


@app.route('/import', methods=['GET', 'POST'])
@login_required
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
@login_required
def downloader_file():
    form = DownloadForm(idu=current_user.username)
    if not form.validate_on_submit():
        return render_template("export.html", form=form)
    return redirect(url_for("download_file", idQ=form.liste.data))


@app.route('/downloadfile/<idQ>')
def download_file(idQ):
    name = "Export" + idQ + ".xml"
    writter(name, 'link_front_back/parser/out/', get_dict_from_DB(idQ), category=True)

    return send_file("parser/out/" + name, as_attachment=True)


@app.route('/choose')
def choose_qcm():
    return render_template("chooseqcm.html",questionnaires=get_questionnaires())

@app.route('/answer/<idqq>', methods=["GET", "POST"])
def answer_qcm(idqq):
    qq = get_questions_and_answers(idqq)
    return render_template("answerqcm.html", questionnaire=qq, idqq=idqq)

@app.route('/sendanswers', methods=["POST"])
def sendanswers():
    idqq = request.form.get("idqq")
    liste = get_liste_id_type_question_in_questionnaire(idqq)
    numEssai = get_essai(current_user.get_id(), idqq) + 1
    for qid, typ in liste:
        if typ == "multichoice":
            rep = request.form.getlist(str(qid)) # pour liste de valeurs (genre checkbox)
            rep = " ".join(rep)
        else:
            rep = request.form.get(str(qid)) # pour valeur simple
        add_rep_user(current_user.get_id(), qid, numEssai, rep)

    return redirect(url_for("score", idqq=idqq, num_essai=numEssai))

@app.route("/score/<idqq>/<num_essai>")
def score(idqq, num_essai):

    return render_template("score.html", score=calcul_score_quizz(current_user.get_id(), idqq, num_essai))
