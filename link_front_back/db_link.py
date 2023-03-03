from sqlalchemy import func, exc, desc
from .setupdb import *
from flask_login import current_user

p = {'category': {'name': '$module$/top/Défaut pour Test_maxime',
                  'info': 'La catégorie par défaut pour les questions partagées dans le contexte «\xa0Test_maxime\xa0».'},
     'questions': [
         {'type': 'truefalse', 'name': 'Question_1_Edited', 'template': 'None', 'questiontext': 'Vrai ou Faux ????????',
          'generalfeedback': None, 'defaultgrade': '1.0000000', 'penalty': '1.0000000', 'hidden': '0',
          'answers': [{'fraction': '0', 'text': 'true', 'feedback': '\n        '},
                      {'fraction': '100', 'text': 'false', 'feedback': '\n        '}]}]}


def get_liste_questionnaire(idu: int = None):
    if idu is None:
        res = ses.query(Questionnaire).all()
    else:
        res = ses.query(Questionnaire).filter(Questionnaire.idUser == idu)
    test = list()
    for rw in res:
        test.append({"idq": rw.idQuestionnaire, "nom": rw.nom, "info": rw.info, "idu": rw.idUser})
    return test


def get_liste_id_nom_questionnaire(idu):
    res = ses.query(Questionnaire).filter(Questionnaire.idUser == idu)
    test = list()
    for rw in res:
        test.append((rw.idQuestionnaire, rw.nom))
    return test


def get_questionnaire_name(idq: int) -> str:
    res = ses.query(Questionnaire).filter(Questionnaire.idQuestionnaire == idq)
    return res[0].nom


def get_questionnaire(idq):
    res = ses.query(Questionnaire).filter(Questionnaire.idQuestionnaire == idq)
    test = list()
    for rw in res:
        test.append({"idq": rw.idQuestionnaire, "nom": rw.nom, "info": rw.info, "idu": rw.idUser})
    return test


def get_questions(idqq: int):
    res2 = ses.query(Question).filter(Question.idQuestionnaire == idqq)
    test2 = list()
    for rz in res2:
        test2.append({"idq": rz.idQuestion, 'type': (ses.query(Type).filter(Type.idType == rz.idType))[0].nomType,
                      'name': rz.name, "questiontext": rz.question, "template": rz.template,
                      "defaultgrade": rz.valeurPoint, "hidden": rz.hidden, "penalty": rz.pointNegatif,
                      "idQuestionnaire": rz.idQuestionnaire, "generalfeedback": rz.feedback, "idt": rz.idType})
    return test2


def get_user(idu: str):
    user = ses.query(User).filter(User.idUser == idu).first()
    return user

def get_answers(idq):
    res = ses.query(RepQuestion).filter(RepQuestion.idQuestion == idq)
    test = list()
    for rw in res:
        test.append({"idr":rw.idReponse,
                     "text":rw.reponse,
                     "fraction":rw.fraction,
                     "feedback":rw.feedback,
                     "idq":rw.idQuestion})
    return test

def get_questions_and_answers(idqq):
    res2 = ses.query(Question).filter(Question.idQuestionnaire == idqq)
    test2 = list()
    for rz in res2:
        test2.append({"idq":rz.idQuestion,
                      'type':(ses.query(Type).filter(Type.idType == rz.idType))[0].nomType,
                      'name' : rz.name,
                      "questiontext":rz.question,
                      "template":rz.template,
                      "defaultgrade":rz.valeurPoint,
                      "hidden":rz.hidden,
                      "penalty":rz.pointNegatif,
                      "idQuestionnaire":rz.idQuestionnaire,
                      "generalfeedback":rz.feedback,
                      "idt":rz.idType,
                      "reponses":get_answers(rz.idQuestion)})
    return test2

def query_max(table):
    res = ses.query(func.max(table)).scalar()
    if res is None:
        return 0
    return res


def add_question(question, idQuestionnaire, idType, hidden=0, valeur=1, feedback='', pointneg=0, template='Non',
                 name=("question " + str(query_max(Question.idQuestion) + 1))):
    q = Question(idQuestion=(query_max(Question.idQuestion) + 1), name=name, question=question, template=template,
                 valeurPoint=valeur, hidden=hidden, pointNegatif=pointneg, idQuestionnaire=idQuestionnaire,
                 feedback=feedback, idType=idType)
    ses.add(q)
    ses.commit()
    return q.idQuestion


def add_answer(answer, fraction, idQuestion, feedback=''):
    q = RepQuestion(idReponse=query_max(RepQuestion.idReponse) + 1, reponse=answer, fraction=fraction,
                    feedback=feedback, idQuestion=idQuestion)
    ses.add(q)
    ses.commit()


def add_questionnaire(questionnaire):
    if not 'category' in questionnaire:
        questionnaire['category'] = dict()
        questionnaire['category']['name'] = "Default questionnaires"
        questionnaire['category']['info'] = "Default questionnaires"
    q = Questionnaire(idQuestionnaire=query_max(Questionnaire.idQuestionnaire) + 1,
                      nom=questionnaire['category']['name'], info=questionnaire['category']['info'],
                      idUser=current_user.username)
    try:
        ses.add(q)
        ses.commit()
        for question in questionnaire['questions']:
            idq = add_question(question['questiontext'], q.idQuestionnaire, get_idtype(question['type']),
                               question['hidden'], question['defaultgrade'], question['generalfeedback'],
                               question['penalty'], question['template'], question['name'])
            for answer in question['answers']:
                add_answer(answer['text'], answer['fraction'], idq, answer['feedback'])
    except exc.SQLAlchemyError as e:
        ses.rollback()
        raise ValueError(str(e.orig))


def get_idtype(nom: str) -> int:
    res = ses.query(Type).filter(Type.nomType == nom)
    return res[0].idType


def del_question(idq):
    for answers in ses.query(RepQuestion).filter(RepQuestion.idQuestion == idq):
        ses.delete(answers)
        ses.commit()
    res = ses.query(Question).filter(Question.idQuestion == idq)
    ses.delete(res[0])
    ses.commit()


def del_questionnaire(idq):
    for questions in ses.query(Question).filter(Question.idQuestionnaire == idq):
        del_question(questions.idQuestion)
    res = ses.query(Questionnaire).filter(Questionnaire.idQuestionnaire == idq)
    ses.delete(res[0])
    ses.commit()


def get_questionnaires():
    res = ses.query(Questionnaire).all()
    test = list()
    for rw in res:
        test.append({"idq": rw.idQuestionnaire, "nom": rw.nom, "info": rw.info, "idu": rw.idUser})
    return test


def get_questionnaire_name(idq: int) -> str:
    res = ses.query(Questionnaire).filter(Questionnaire.idQuestionnaire == idq)
    return res[0].nom


def get_question(idq):
    res = ses.query(Question).filter(Question.idQuestion == idq)
    test = list()
    for rw in res:
        test.append({"idq": rw.idQuestion, 'type': (ses.query(Type).filter(Type.idType == rw.idType))[0].nomType,
                     'name': rw.name, "questiontext": rw.question, "template": rw.template,
                     "defaultgrade": rw.valeurPoint, "hidden": rw.hidden, "penalty": rw.pointNegatif,
                     "idQuestionnaire": rw.idQuestionnaire, "generalfeedback": rw.feedback, "idt": rw.idType})
    return test[0]


def add_rep_user(idu, idq, num_essai, reponse):
    ru = RepUser(idUser=idu, idQuestion=idq, essaiNumero=num_essai, reponse=reponse)
    ses.add(ru)
    ses.commit()

def get_rep_user(idu, idq, num_essai):
    res = ses.query(RepUser).filter(RepUser.idQuestion == idq, RepUser.idUser == idu, RepUser.essaiNumero == num_essai).first()
    return res.reponse

def calcul_score_quizz(idu, idqq, num_essai):
    score = 0
    total = 0
    questions = get_questions_and_answers(idqq)
    for question in questions:
        idq = question['idq']
        reponse = get_rep_user(idu, idq, num_essai)
        total += question['defaultgrade']
        score = test_match_case(question, reponse, score)
    return str(score) +"/"+ str(total)

def test_match_case(question, reponse, score):
    match (question['type']):
        case "multichoice":
            id_reponses = set(reponse.split())
            id_v_rep = set()
            for rep in question['reponses']:
                if rep['fraction'] != 0:
                    id_v_rep.add(str(rep['idr']))
            if id_reponses == id_v_rep:
                score += question['defaultgrade']
            else:
                score -= question['penalty']
            return score
        case "truefalse":
            id_reponse = reponse
            for rep in question['reponses']:
                if rep['fraction'] == 100:
                    if id_reponse == str(question['reponses'][0]['idr']):
                        score += question['defaultgrade']
                    else:
                        score -= question['penalty']
            return score
        case "Reponse courte":
            if reponse == question['reponses'][0]:
                score += question['defaultgrade']
            else:
                score -= question['penalty']
    return score

def get_essai(idu, idqq):
    res = ses.query(RepUser, Question).filter(
        RepUser.idUser == idu, Question.idQuestionnaire == idqq).order_by(
        desc(RepUser.essaiNumero)).first()
    if res is None:
        return 0
    for row in res:
        return 0 if row.essaiNumero is None else row.essaiNumero


def get_liste_id_type_question_in_questionnaire(idqq: int):
    res = ses.query(Question).filter(Question.idQuestionnaire == idqq)
    liste = list()
    for row in res:
        liste.append((row.idQuestion, (ses.query(Type).filter(Type.idType == row.idType))[0].nomType))
    return liste

def main():
    add_questionnaire(p)


if __name__ == '__main__':
    main()
