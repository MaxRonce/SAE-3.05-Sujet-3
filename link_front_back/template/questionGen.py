
import random

#Questions template pattern
# A question that is template is a String contained in the database field question.template

# the template is tuple saved as a string that have the following format:
# [(equation,[conditions]), (key, rangeA, rangeB, step),(key, rangeA, rangeB, step))

#Exemple: "Il y a $1 vaches dans un pré, Marc en mange $2, Combien en reste-il ?"

#The template is: [("X1-X2",["X1>X2"]), ("X1", 1, 10, 1), ("X2", 1, 10, 1)]

def create_question_template():
    # Ask the user to enter the template text
    question_text = input("Entrez le texte de la question: ")

    #Initialize the template
    template = []

    # Ask to enter the equation
    equation = input("Entrez l'équation: ")
    conditions = []
    has_conditions = input("Y a-t-il des contraintes (o/n)?")
    template.append(equation)

    # Demande à l'utilisateur s'il y a des variables à varier
    has_variables = input("Y a-t-il des variables (o/n)?")
    if has_variables == "o":
        # Demande à l'utilisateur de rentrer les informations sur les variables à varier
        while True:
            key = input("Entrez la clé de la variable: ")
            range_a = int(input("Entrez la valeur de départ de la plage: "))
            range_b = int(input("Entrez la valeur de fin de la plage: "))
            step = int(input("Entrez le pas: "))
            template.append((key, range_a, range_b, step))

            # Demande à l'utilisateur s'il y a d'autres variables à ajouter
            has_more_variables = input("Y a-t-il d'autres variables à ajouter (o/n)?")
            if has_more_variables == "n":
                break
    return (question_text, template)


def generate_from_template(question_text, template):
    # Initialize the question
    question = question_text
    #split the question into words
    words = question.split(" ")

    #Text to equation
    equation = template[0]
    #convert the equation in math equation with eval

    #test to calculate with X1 = 1 and X2 = 3
    X1 = 1
    X2 = 3
    print(equation)
    print(eval(equation))


    #generate all the possible values for the variables in the given range
    result = {}
    for i in range(1,len(template)):
        #store the result in a dict of list
        key = template[i][0]
        range_a = template[i][1]
        range_b = template[i][2]
        step = template[i][3]
        values = []
        for value in range(range_a, range_b+1, step):
            values.append(value)
        result[key] = values


    all_questions_list = []
    all_answers_list = []
    all_values_list = []
    #generate all the possible questions
    for key in result:
        print(result[key])
        print(len(result))
        all_values_list.append(result[key])

    temp = [(x,y) for x in all_values_list[0] for y in all_values_list[1]]
    all_answers_list = [eval(equation) for X1,X2 in temp]

    all_questions_list = [question_text.replace("X1", str(X1)).replace("X2", str(X2)) for X1,X2 in temp]
    return all_questions_list, all_answers_list



def main():
    #question_text, template = create_question_template()
    #test values
    question_text = "Il y a X1 vaches dans un pré, Marc en mange X2, Combien en reste-il ?"
    template = ["X1-X2", ("X1", 1, 10, 4), ("X2", 1, 10, 1)]
    print(question_text) # Res de &1 et &2
    print(template) #return [('X1+X2'), ('X1', 1, 10, 4), ('X2', 1, 3, 2)]
    all_questions_list, all_answers_list = generate_from_template(question_text, template)

    for i in range(4):
        index = random.randint(0, len(all_questions_list)-1)
        print(all_questions_list[index])
        print(f"Correct answer : {all_answers_list[index]}")



if __name__ == "__main__":
    main()





