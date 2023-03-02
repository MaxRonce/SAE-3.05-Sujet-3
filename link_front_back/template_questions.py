from link_front_back import db_link
from link_front_back.setupdb import Question, RepQuestion
from random import randint, choice


class Answer:
    def __init__(self, idr, reponse, idq, fraction, feedback):
        self.idr = idr
        self.reponse = reponse
        self.idq = idq
        self.fraction = fraction
        self.feedback = feedback

    def __str__(self):
        return f"Answer({self.idr}, {self.reponse}, {self.idq}, {self.fraction}, {self.feedback})"

    def __repr__(self):
        return f"Answer({self.idr}, {self.reponse}, {self.idq}, {self.fraction}, {self.feedback})"


class Full_Question:
    """
    Class to create a full question object from a question object and its answers
    """
    def __init__(self,idq, name, question, template, valeurPoint, hidden, pointNegatif, idQuestionnaire, feedback, idType, typeQuestion, answers=None):
        self.idq = idq
        self.name = name
        self.question = question
        self.template = template
        self.valeurPoint = valeurPoint
        self.hidden = hidden
        self.pointNegatif = pointNegatif
        self.idQuestionnaire = idQuestionnaire
        self.feedback = feedback
        self.idType = idType
        self.typeQuestion = typeQuestion
        self.answers = answers

    def add_answer(self, idr, reponse, idq, fraction, feedback):
        self.answers.append(Answer(idr, reponse, idq, fraction, feedback))

    def __repr__(self):
        return f"Full_Question({self.idq}, {self.name}, {self.question}, {self.template}, {self.valeurPoint}, {self.hidden}, {self.pointNegatif}, {self.idQuestionnaire}, {self.feedback}, {self.idType}, {self.typeQuestion}, {self.answers})"

    def __str__(self):
        return f"Full_Question(idq:{self.idq}, name:{self.name}, text:{self.question}, template:{self.template}, point:{self.valeurPoint}, hidden:{self.hidden}, negatif:{self.pointNegatif}, idQ:{self.idQuestionnaire}, feedback:{self.feedback}, idT:{self.idType}, typeQuestion:{self.typeQuestion}, answers:{self.answers})"
class Question_Template(Question):
    """
    Class to create a question object from a question object
    it is used to create a new question
    a question is 'template' if the template field is not null,
    in the case it's not null, the template field have the following format:
    {'val1':'answ1','val2':'answ2','val3':'answ3'}
    where X is a value contained in the question text, that will be replaced with the value

    example :
    question text : "What is the value of X² ?"
    1,1,2,4,3,9 and should be transformed into : {1:1,2:4,3:9}
    and the question is a multiple choice question, the question will be :
    "What is the value of 1² ?" with answer 1, and choice 1,4,9,16
    "What is the value of 2² ?" with answer 4, and choice 1,4,9,16
    "What is the value of 3² ?" with answer 9, and choice 1,4,9,16
    """
    def __init__(self, question: Question = None):
        super().__init__()
        if question is not None:
            self.idQuestion = question.idQuestion
            self.name = question.name
            self.question = question.question
            self.template = question.template
            self.valeurPoint = question.valeurPoint
            self.hidden = question.hidden
            self.pointNegatif = question.pointNegatif
            self.idQuestionnaire = question.idQuestionnaire
            self.feedback = question.feedback
            self.idType = question.idType
            self.typeQuestion = question.typequestion.nomType


    def __repr__(self):
        return f"Question_Template(idq :{self.idQuestion}, nom :{self.name}, texte : {self.question}, template :{self.template}, points :{self.valeurPoint}, negative :{self.pointNegatif}, questionnaire: {self.idQuestionnaire}, feedback : {self.feedback}, {self.typeQuestion})"

    def set_template(self, template: str):
        self.template = template

    def template_transform(self):
        """
        transform a string like 1,1,2,4,3,9 into a dict like {1:1,2:4,3:9},
        values could be string or int
        """
        ans_dict = {}
        ans_list = self.template.split(",")
        for i in range(0, len(ans_list), 2):
            ans_dict[ans_list[i]] = ans_list[i + 1]
        self.template = ans_dict

    def template_transform_back(self):
        """
        transform a dict like {1:1,2:4,3:9} into a string like 1,1,2,4,3,9
        """
        ans_list = []
        for k, v in self.template.items():
            ans_list.append(str(k))
            ans_list.append(str(v))
        self.template = ",".join(ans_list)

    def set_text(self, text: str):
        self.question = text

    def set_type(self, type: str):
        self.typeQuestion = type

    def get_template(self):
        return self.template

    def parse_text(self):
        """
        parse the question text to find the X value to replace, return the index of the X in the text
        """
        for i, c in enumerate(self.question):
            if c == "X":
                return i

    def generate(self):
        """
        generate a question from the template, with its answers and choices
        """
        # get the index of the X in the question text
        index = self.parse_text()
        # replace take a random value from the template dict and replace the X with it
        random = choice(list(self.template.keys()))
        self.question = self.question[:index] + str(random) + self.question[index + 1:]
        # create the answer
        answer_list = []
        answer = Answer(self.idQuestion, self.template[random], self.idQuestion, 100, self.feedback)
        answer_list.append(answer)
        #create the 3 others answers with random values
        choices = list(self.template.values())
        choices.remove(self.template[random])
        for i in range(len(choices)):
            random = choice(choices)
            choices.remove(random)
            answer = Answer(self.idQuestion, random, self.idQuestion, 0, self.feedback)
            answer_list.append(answer)

        #create a Full_Question object with the question and its answers
        full_question = Full_Question(self.idQuestion, self.name, self.question, self.template, self.valeurPoint, self.hidden, self.pointNegatif, self.idQuestionnaire, self.feedback, self.idType, self.typeQuestion, answer_list)
        return full_question












if __name__ == '__main__':
    q = db_link.ses.query(Question).filter(Question.idQuestion == 1).one()
    qt = Question_Template(q)
    template = "1,1,2,4,3,9"
    print(qt)
    qt.set_template(template)
    print(qt)
    qt.template_transform()
    print(qt)
    qt.set_type("multichoice")
    qt.set_text("What is the value of X² ?")
    print(qt)

    print(qt.generate())

