# XML to pandas dataframe
import xml.etree.ElementTree as ET
import re

# parse the xml file in data/ folder
# display the tree


# the file contain multiple questions, the first one is a special case "category"
# print the first question

def get_cat_name(root):
    """
    get the name of the category
    :param root:
    :return:
    """
    for child in root:
        if child.tag == 'category':
            return child[0].text
        else:
            return get_cat_name(child)


def get_cat_info(root):
    for child in root:
        # print(child.tag, child.attrib)
        if child.tag == 'info':
            for child2 in child:
                return child2.text
        else:
            get_cat_info(child)


# now the rest of the questions are in the same format
# we can use a loop to get all the questions
# store them in a dataframe, the category names are name, questiontext, generalfeedback, defaultgrade, penalty,
# hidden and answers
# the answers are a list of dict, text, fraction, feedback

# function that get a question and return a dict with the question info

def get_question(question):
    question_dict = {}
    question_dict['type'] = question.attrib['type']
    for child in question:
        if child.tag == 'name':
            question_dict['name'] = child[0].text
        elif child.tag == 'questiontext':
            question_dict['questiontext'] = clean_text(child[0].text)
        elif child.tag == 'generalfeedback':
            question_dict['generalfeedback'] = clean_text(child[0].text)
        elif child.tag == 'defaultgrade':
            question_dict['defaultgrade'] = child.text
        elif child.tag == 'penalty':
            question_dict['penalty'] = child.text
        elif child.tag == 'hidden':
            question_dict['hidden'] = child.text
        elif child.tag == 'answer':
            question_dict['answers'] = get_answers(question)
        question_dict['template'] = "None"
    return question_dict


def question_text_cleaner(text):
    try:
        subTree = ET.fromstring(text)
        return subTree.text
    except:
        return text

def clean_text(text):
    if text is None:
        return None
    else:
        cleaned = re.sub('<.*?>', '', text)
        return cleaned.strip()



def get_answers(question):
    answers = []
    for child in question:
        if child.tag == 'answer':
            answer = {}
            answer['fraction'] = child.attrib['fraction']
            for child2 in child:
                if child2.tag == 'text':
                    answer['text'] = clean_text(child2.text)
                elif child2.tag == 'feedback':
                    answer['feedback'] = clean_text(child2.text)
            answers.append(answer)
    return answers


def parse(path):
    """
    parse the xml file and return a dict with the category name and the questions
    :param path:
    :return:
    """
    tree = ET.parse(path)
    root = tree.getroot()
    questions = {}
    questions_list = []
    for question in root:
        if question.tag == 'question' and question.attrib['type'] == 'category':
            category = {'name': get_cat_name(question), 'info': get_cat_info(question)}
            # print(category)
            questions['category'] = category

        elif question.tag == 'question' and question.attrib['type'] != 'category':
            question_dict = get_question(question)
            # print(question_dict)
            questions_list.append(question_dict)
    questions['questions'] = questions_list
    return questions


if __name__ == '__main__':
    path = 'data/Multiple.xml'
    path2 = 'data/Vrai_Faux.xml'
    path3 = 'data/Demp.xml'
    path4 = 'data/TestS4.xml'
    # display as json
    import json

    print(json.dumps(parse(path), indent=4))
    print(json.dumps(parse(path2), indent=4))
    print(json.dumps(parse(path3), indent=4))
    print(json.dumps(parse(path4), indent=4))
