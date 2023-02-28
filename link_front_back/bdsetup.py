from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

login, passwd, serveur, bd = "","" , "", ""
engine = create_engine('mysql+mysqldb://'+login+':'+passwd+'@'+serveur+'/'+bd)

ses = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

Type = Base.classes.
User = Base.classes.
Questionnaire = Base.classes.
Question = Base.classes.
RepQuestion = Base.classes.