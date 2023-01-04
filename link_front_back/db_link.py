from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()

login, passwd, serveur, bd = "antoninreydet", "root", "localhost", "KAIRO"
engine = create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd)

ses = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

User = Base.classes.USERS
Questionnaire = Base.classes.QUESTIONNAIRE
Question = Base.classes.QUESTION
RepQuestion = Base.classes.REPONSEQUESTION

def get_liste_questionnaire(idu: int = None):
    if idu is None:
        res = ses.query(Questionnaire).all()
    else:
        res = ses.query(Questionnaire).filter(Questionnaire.idUser == idu)
    test = list()
    for rw in res:
        test.append({"idq":rw.idQuestionnaire, "nom":rw.nom, "info":rw.info, "idu":rw.idUser})
    return test

def get_questions(idqq: int):
    res2 = ses.query(Question).filter(Question.idQuestionnaire == idqq)
    test2 = list()
    for rz in res2:
        test2.append([rz.idQuestion, rz.question])
    print(test2)
    return test2

def add_question(question, idQuestionnaire, idType, hidden = 0, valeur=1,feedback = '', pointneg=0,template = 'Non', name = ("question "+ str(ses.query(Question).filter().count() + 1))):

    q = Question(idQuestion=(ses.query(Question).filter().count() + 1), name = name, question=question, template=template, valeurPoint=valeur,hidden = hidden, pointNegatif=pointneg, idQuestionnaire=idQuestionnaire, feedback=feedback, idType=idType)
    ses.add(q)
    ses.commit()

def add_answer(answer, fraction, idQuestion, feedback = ''):
    q = RepQuestion(idReponse=(ses.query(RepQuestion).filter().count() + 1), reponse=answer, fraction=fraction, feedback=feedback, idQuestion=idQuestion)
    ses.add(q)
    ses.commit()
q = { "category": {'name': '$module$/top/Défaut pour Test_maxime', 'info': 'La catégorie par défaut pour les questions partagées dans le contexte «\xa0Test_maxime\xa0».'},
"questions":[{'name': 'Question_1_Edited', 'questiontext': 'Vrai ou Faux ????????', 'generalfeedback': None, 'defaultgrade': 1.0000000, 'penalty': 1.0000000, 'hidden': 0, 'answers': [{'fraction': 0, 'text': 'true', 'feedback': '\n'}, {'fraction': 100, 'text': 'false', 'feedback': '\n'}]}]
}


def add_questionnaire(questionnaire):
    q = Questionnaire(idQuestionnaire=(ses.query(Questionnaire).filter().count() + 1), nom=questionnaire['category']['name'], info=questionnaire['category']['info'], idUser=1)
    ses.add(q)
    ses.commit()
    for question in questionnaire['questions']:
        add_question(question['questiontext'], q.idQuestionnaire, 1, question['hidden'], question['defaultgrade'], question['generalfeedback'], question['penalty'],"Non", question['name'])
        for answer in question['answers']:
            add_answer(answer['text'], answer['fraction'], ses.query(Question).filter(Question.idQuestionnaire == q.idQuestionnaire).count(), answer['feedback'])
def main():
    #add_questionnaire(q)
    t = get_questions(2)
    print(t[0])
    #add_question("test", 1, 1)
    #add_answer("test", 100, 1)
    #print(get_liste_questionnaire())
    #print(get_questions(1))

if __name__ == '__main__':
    main()

