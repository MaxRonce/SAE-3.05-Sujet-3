import link_front_back.db_link as db_link

# access to the DATABASE using the db_link.py file

# create XML file from a dict
#  example :

# {'category':
#   {'name': '$module$/top/Défaut pour Test_maxime',
#   'info' : 'La catégorie par défaut pour les questions partagées dans le contexte «\xa0Test_maxime\xa0».'},
# 'questions':
#   [{'name': 'Question_1_Edited',
#   'questiontext' : 'Vrai ou Faux ????????',
#   'generalfeedback': None,
#   'defaultgrade': '1.0000000',
#   'penalty': '1.0000000',
#   'hidden': '0',
#   'answers': [{'fraction': '0', 'text': 'true', 'feedback': '\n        '}, {'fraction': '100', 'text': 'false', 'feedback': '\n        '}]},
def get_dict_from_DB(id):
    # get the selected questionnaire
    questionnaires = db_link.get_questionnaire(id)

    # for each questionnaire, get all the questions
    questions = db_link.get_questions(questionnaires[0]['idq'])

    # merge the questionnaires and questions in a dictionary
    category = {
        'nom': questionnaires[0]['nom'],
        'info': questionnaires[0]['info']
    }

    # add the answers to the questions with the same id
    for question in questions:
        question['answers'] = []

        # get all answers for the current question
        answers = db_link.get_answers(question['idq'])

        for answer in answers:
            question['answers'].append({
                'text': answer['text'],
                'fraction': answer['fraction'],
                'feedback': answer['feedback']
            })

        # remove unnecessary fields
        question.pop('idq')
        question.pop('idt')
        question.pop('idQuestionnaire')
        question.pop('template')

    full_question = {
        'category': category,
        'questions': questions
    }

    return full_question


if __name__ == "__main__":
    import json
    print(json.dumps(get_dict_from_DB(6), indent=4))










