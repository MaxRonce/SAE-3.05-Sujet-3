from DB_to_XML import main
def writter(filename :str, path:str, data:dict, category:bool=False):
    """Create a file with the data in the dict"""
    #create the file
    with open(path + filename, 'w', encoding="UTF-8") as file:

        file.writelines('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.writelines('<quiz>\n')
        #write the category if there is one
        if category:
            file.writelines('\t<question type="category">\n')
            file.writelines('\t\t<category>\n')
            file.writelines('\t\t\t<text>'+data['category']['nom']+'</text>\n')
            file.writelines('\t\t</category>\n')
            file.writelines('\t<info format="html">\n')
            file.writelines('\t\t<text>'+data['category']['info']+'</text>\n')
            file.writelines('\t</info>\n')
            file.writelines('\t<idnumber></idnumber>\n')
            file.writelines('\t</question>\n')
            file.writelines('\n')

        #write the questions
        for question in data['questions']:
            file.writelines('\t<question type="truefalse">\n')
            file.writelines('\t\t<name>\n')
            file.writelines('\t\t\t<text>'+question['name']+'</text>\n')
            file.writelines('\t\t</name>\n')
            file.writelines('\t\t<questiontext format="html">\n')
            file.writelines('\t\t\t<text><![CDATA[<p dir="ltr" style="text-align: left;">'+question['questiontext']+'</p>]]></text>\n')
            file.writelines('\t\t</questiontext>\n')
            file.writelines('\t\t<generalfeedback format="html">\n')
            if question['generalfeedback'] is not None:
                file.writelines('\t\t\t<text><![CDATA[<p dir="ltr" style="text-align: left;">'+question['generalfeedback']+'</p>]]></text>\n')
            else:
                file.writelines('\t\t\t<text></text>\n')
            file.writelines('\t\t</generalfeedback>\n')
            file.writelines('\t\t<defaultgrade>'+str(question['defaultgrade'])+'</defaultgrade>\n')
            file.writelines('\t\t<penalty>'+str(question['penalty'])+'</penalty>\n')
            file.writelines('\t\t<hidden>'+str(question['hidden'])+'</hidden>\n')
            file.writelines('\t\t<idnumber></idnumber>\n')

            #write the answers
            for answer in question['answers']:
                file.writelines('\t\t<answer fraction="'+str(answer['fraction'])+'" format="moodle_auto_format">\n')
                file.writelines('\t\t\t<text>'+answer['text']+'</text>\n')
                file.writelines('\t\t\t<feedback format="html">\n')
                if answer['feedback'] is not None:
                    file.writelines('\t\t\t\t<text><![CDATA[<p dir="ltr" style="text-align: left;">'+answer['feedback']+'</p>]]></text>\n')
                else:
                    file.writelines('\t\t\t\t<text></text>\n')
                file.writelines('\t\t\t</feedback>\n')
                file.writelines('\t\t</answer>\n')

            file.writelines('\t</question>\n')
            file.writelines('\n')
        file.writelines('</quiz>\n')



if __name__ == "__main__":
        writter('test.xml', 'out/', main(), category=True)
