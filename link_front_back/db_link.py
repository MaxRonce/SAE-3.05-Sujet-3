from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .app import login_manager

login, passwd, serveur, bd = "", "", "", ""
engine = create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd)

ses = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

User = Base.classes.USERS
Questionnaire = Base.classes.QUESTIONNAIRE
Question = Base.classes.QUESTION

def get_liste_questionnaire(idu: int = None):
    if idu is None:
        res = ses.query(Questionnaire).all()
    else:
        res = ses.query(Questionnaire).filter(Questionnaire.idUser == idu)
    test = list()
    for rw in res:
        test.append({"idq":rw.idQuestionnaire, "nom":rw.nom, "descr":rw.descr, "idu":rw.idUser})
    return test

def get_questions(idqq):
    res2 = ses.query(Question).filter(Question.idQuestionnaire == idqq)
    test2 = list()
    for rz in res2:
        test2.append(rz.question)
    print(test2)
    return test2

def get_user(idu: str):
    user = ses.query(User).filter(User.idUser == idu).first()
    return user