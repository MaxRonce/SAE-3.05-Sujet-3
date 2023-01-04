from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()

login, passwd, serveur, bd = "root", "ronceray", "localhost", "KAIRO"
engine = create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd)

ses = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

User = Base.classes.users
Questionnaire = Base.classes.questionnaire
Question = Base.classes.question
RepQuestion = Base.classes.reponsequestion
Type = Base.classes.typequestion


def get_liste_questionnaire(idu: int = None):
    if idu is None:
        res = ses.query(Questionnaire).all()
    else:
        res = ses.query(Questionnaire).filter(Questionnaire.idUser == idu)
    test = list()
    for rw in res:
        test.append({"idq":rw.idQuestionnaire, "nom":rw.nom, "info":rw.info, "idu":rw.idUser})
    return test

def get_questionnaire(idq):
    res = ses.query(Questionnaire).filter(Questionnaire.idQuestionnaire == idq)
    test = list()
    for rw in res:
        test.append({"idq":rw.idQuestionnaire, "nom":rw.nom, "info":rw.info, "idu":rw.idUser})
    return test

def get_questions(idqq: int):
    res2 = ses.query(Question).filter(Question.idQuestionnaire == idqq)
    test2 = list()
    for rz in res2:
        test2.append({"idq":rz.idQuestion, 'type':(ses.query(Type).filter(Type.idType == rz.idType))[0].nomType, 'name' : rz.name ,"questiontext":rz.question, "template":rz.template, "defaultgrade":rz.valeurPoint, "hidden":rz.hidden, "penalty":rz.pointNegatif, "idQuestionnaire":rz.idQuestionnaire, "generalfeedback":rz.feedback, "idt":rz.idType})
    return test2

def get_anwser(idq):
    res = ses.query(RepQuestion).filter(RepQuestion.idQuestion == idq)
    test = list()
    for rw in res:
        test.append({"idr":rw.idReponse, "text":rw.reponse, "fraction":rw.fraction, "feedback":rw.feedback, "idq":rw.idQuestion})
    return test



def add_question(name, question, idQuestionnaire, idType, hidden = 0, valeur=1,feedback = '', pointneg=0,template = 'Non'):

    q = Question(idQuestion=(ses.query(Question).filter().count() + 1), name = name, question=question, template=template, valeurPoint=valeur,hidden = hidden, pointNegatif=pointneg, idQuestionnaire=idQuestionnaire, feedback=feedback, idType=idType)
    ses.add(q)
    ses.commit()

def add_answer(answer, fraction, idQuestion, feedback = ''):
    q = RepQuestion(idReponse=(ses.query(RepQuestion).filter().count() + 1), reponse=answer, fraction=fraction, feedback=feedback, idQuestion=idQuestion)
    ses.add(q)
    ses.commit()
q = {'category': {'name': '$module$/top/Défaut pour Test_maxime', 'info': 'La catégorie par défaut pour les questions partagées dans le contexte «\xa0Test_maxime\xa0».'}, 'questions': [{'type': 'Reponse courte', 'name': 'Question_1_Edited', 'questiontext': 'Vrai ou Faux ????????', 'defaultgrade': 1, 'hidden': 0, 'penalty': 1, 'generalfeedback': None, 'answers': [{'text': 'true', 'fraction': 0.0, 'feedback': '\n'}, {'text': 'false', 'fraction': 100.0, 'feedback': '\n'}]}]}

def add_questionnaire(questionnaire):
    q = Questionnaire(idQuestionnaire=(ses.query(Questionnaire).filter().count() + 1), nom=questionnaire['category']['name'], info=questionnaire['category']['info'], idUser=1)
    ses.add(q)
    ses.commit()
    for question in questionnaire['questions']:
        add_question(question['name'], question['questiontext'], q.idQuestionnaire, get_idtype(question['type']), question['hidden'], question['defaultgrade'], question['generalfeedback'], question['penalty'])
        for answer in question['answers']:
            add_answer(answer['text'], answer['fraction'], ses.query(Question).filter(Question.idQuestionnaire == q.idQuestionnaire).count(), answer['feedback'])

def get_idtype(nom:str)->int:
    res = ses.query(Type).filter(Type.nomType == nom)
    return res[0].idType
def main():
    add_questionnaire(q)
    #add_question("test", 1, 1)
    #add_answer("test", 100, 1)
    #print(get_liste_questionnaire())
    #print(get_questions(1))

if __name__ == '__main__':
    main()
    get_questions(1)
    print(get_idtype("truefalse"))
