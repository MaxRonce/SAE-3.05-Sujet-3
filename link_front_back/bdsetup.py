from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

login, passwd, serveur, bd = "root","ronceray" , "localhost", "kairo"
engine = create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd)

ses = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

Type = Base.classes.typequestion
User = Base.classes.users
Questionnaire = Base.classes.questionnaire
Question = Base.classes.question
RepQuestion = Base.classes.reponsequestion