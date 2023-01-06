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

def main():
    #get the selected questionnaire
    questionnaires = db_link.get_questionnaire(1)
    #for each questionnaire
    #get all the questions in the 1st questionnaire
    questions = db_link.get_questions(questionnaires[0]['idq'])

    #get all the answers in the 1st question
    answers = db_link.get_anwser(questions[0]['idq'])

    #merge the 3 list in a dict

    #pop in questionnaires
    questionnaires[0].pop('idq')
    questionnaires[0].pop('idu')


    #add the answers to the questions with the same id
    for question in questions:
        question['answers'] = []
        for answer in answers:
            if question['idq'] == answer['idq']:
                answer.pop('idq')
                answer.pop('idr')
                question['answers'].append(answer)
        question.pop('idq')
        question.pop('idt')
        question.pop('idQuestionnaire')
        question.pop('template')


    full_question = {'category': questionnaires[0], 'questions': questions}
    print(full_question)
    return full_question

if __name__ == "__main__":
    main()


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
    #get the selected questionnaire
    questionnaires = db_link.get_questionnaire(id)
    #for each questionnaire
    #get all the questions in the 1st questionnaire
    questions = db_link.get_questions(questionnaires[0]['idq'])

    #get all the answers in the 1st question
    answers = db_link.get_anwser(questions[0]['idq'])

    #merge the 3 list in a dict

    #pop in questionnaires
    questionnaires[0].pop('idq')
    questionnaires[0].pop('idu')


    #add the answers to the questions with the same id
    for question in questions:
        question['answers'] = []
        for answer in answers:
            if question['idq'] == answer['idq']:
                question['answers'].append(answer)
                #print(question['answers'])

        question.pop('idq')
        question.pop('idt')
        question.pop('idQuestionnaire')
        question.pop('template')


    full_question = {'category': questionnaires[0], 'questions': questions}
    #print(full_question)
    return full_question

if __name__ == "__main__":
    get_dict_from_DB()









