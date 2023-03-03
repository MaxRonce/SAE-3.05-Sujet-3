from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

login, passwd, serveur, bd = "antoninreydet", "root", "localhost", "kairo"
engine = create_engine('mysql+mysqldb://' + login + ':' + passwd + '@' + serveur + '/' + bd)

ses = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

Type = Base.classes.TYPEQUESTION
User = Base.classes.USERS
Questionnaire = Base.classes.QUESTIONNAIRE
Question = Base.classes.QUESTION
RepQuestion = Base.classes.REPONSEQUESTION