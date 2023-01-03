from flask import Flask, render_template, request, redirect
from db_link import get_liste_questionnaire, get_questions

app = Flask(__name__)
@app.route("/") # page de base du site
def aff_home():
    return render_template("home.html")

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

