from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from .app import login_manager

login, passwd, serveur, bd = "root", "ronceray", "localhost", "KAIRO"
engine = create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd)

ses = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

Type = Base.classes.typequestion
User = Base.classes.users
Questionnaire = Base.classes.questionnaire
Question = Base.classes.question
RepQuestion = Base.classes.reponsequestion


p= {'category': {'name': '$module$/top/Défaut pour Test_maxime', 'info': 'La catégorie par défaut pour les questions partagées dans le contexte «\xa0Test_maxime\xa0».'}, 'questions': [{'type': 'truefalse', 'name': 'Question_1_Edited', 'template': 'None', 'questiontext': 'Vrai ou Faux ????????', 'generalfeedback': None, 'defaultgrade': '1.0000000', 'penalty': '1.0000000', 'hidden': '0', 'answers': [{'fraction': '0', 'text': 'true', 'feedback': '\n        '}, {'fraction': '100', 'text': 'false', 'feedback': '\n        '}]}]}

def get_liste_questionnaire(idu: int = None):
    if idu is None:
        res = ses.query(Questionnaire).all()
    else:
        res = ses.query(Questionnaire).filter(Questionnaire.idUser == idu)
    test = list()
    for rw in res:
        test.append({"idq":rw.idQuestionnaire, "nom":rw.nom, "info":rw.info, "idu":rw.idUser})
    return test

def get_liste_id_nom_questionnaire(idu: int = None):
    if idu is None:
        res = ses.query(Questionnaire).all()
    else:
        res = ses.query(Questionnaire).filter(Questionnaire.idUser == idu)
    test = list()
    for rw in res:
        test.append((rw.idQuestionnaire,rw.nom))
    return test

def get_questionnaire_name(idq:int)->str:
    res = ses.query(Questionnaire).filter(Questionnaire.idQuestionnaire == idq)
    return res[0].nom
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

def get_user(idu: str):
    user = ses.query(User).filter(User.idUser == idu).first()
    return user

def get_anwser(idq):
    res = ses.query(RepQuestion).filter(RepQuestion.idQuestion == idq)
    test = list()
    for rw in res:
        test.append({"idr":rw.idReponse, "text":rw.reponse, "fraction":rw.fraction, "feedback":rw.feedback, "idq":rw.idQuestion})
    return test

def query_max(table):
    res = ses.query(func.max(table)).scalar()
    if res is None:
        return 0
    return res

def add_question(question, idQuestionnaire, idType, hidden = 0, valeur=1,feedback = '', pointneg=0,template = 'Non', name = ("question "+ str(query_max(Question.idQuestion)+1))):

    q = Question(idQuestion=(query_max(Question.idQuestion)+1), name=name, question=question, template=template, valeurPoint=valeur, hidden=hidden, pointNegatif=pointneg, idQuestionnaire=idQuestionnaire, feedback=feedback, idType=idType)
    ses.add(q)
    ses.commit()
    return q.idQuestion

def add_answer(answer, fraction, idQuestion, feedback = ''):
    q = RepQuestion(idReponse=query_max(RepQuestion.idReponse)+1, reponse=answer, fraction=fraction, feedback=feedback, idQuestion=idQuestion)
    ses.add(q)
    ses.commit()

def add_questionnaire(questionnaire):
    q = Questionnaire(idQuestionnaire=query_max(Questionnaire.idQuestionnaire)+1, nom=questionnaire['category']['name'], info=questionnaire['category']['info'], idUser=1)
    ses.add(q)
    ses.commit()
    for question in questionnaire['questions']:
        idq = add_question(question['questiontext'], q.idQuestionnaire, get_idtype(question['type']), question['hidden'], question['defaultgrade'], question['generalfeedback'], question['penalty'], question['template'], question['name'])
        for answer in question['answers']:
            add_answer(answer['text'], answer['fraction'],idq, answer['feedback'])

def get_idtype(nom:str)->int:
    res = ses.query(Type).filter(Type.nomType == nom)
    return res[0].idType

def del_question(idq):
    for answers in ses.query(RepQuestion).filter(RepQuestion.idQuestion == idq):
        ses.delete(answers)
        ses.commit()
    res = ses.query(Question).filter(Question.idQuestion == idq)
    ses.delete(res[0])
    ses.commit()

def main():
    add_questionnaire(p)

if __name__ == '__main__':
    main()

