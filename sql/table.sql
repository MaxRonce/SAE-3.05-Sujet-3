
USE KAIRO;
DROP TABLE IF EXISTS REPONSEUSER;
DROP TABLE IF EXISTS REPONSEQUESTION;
DROP TABLE IF EXISTS QUESTION;
DROP TABLE IF EXISTS TYPEQUESTION;
DROP TABLE IF EXISTS QUESTIONNAIRE;
DROP TABLE IF EXISTS USERS;



CREATE TABLE USERS(
    idUser INT(9),
    prof boolean,
    PRIMARY KEY (idUser)
);


CREATE TABLE QUESTIONNAIRE(
    idQuestionnaire INT(9),
    nom VARCHAR(500),
    info VARCHAR(500),
    idUser INT(9),
    PRIMARY KEY (idQuestionnaire)
);


CREATE TABLE TYPEQUESTION(
    idType INT(9),
    nomType VARCHAR(500),
    PRIMARY KEY (idType)
);


CREATE TABLE QUESTION(
    idQuestion INT(9),
    name VARCHAR(100),
    question VARCHAR(500),
    template VARCHAR(500),
    valeurPoint INT(2),
    hidden boolean,
    pointNegatif INT(2),
    idQuestionnaire INT(9),
    feedback VARCHAR(500),
    idType INT(9),
    PRIMARY KEY (idQuestion)
);


CREATE TABLE REPONSEQUESTION(
    idReponse INT(9),
    reponse VARCHAR(500),
    idQuestion INT(9),
    fraction FLOAT,
    feedback VARCHAR(500),
    PRIMARY KEY (idReponse)
    );


CREATE TABLE REPONSEUSER(
    idUser INT(9),
    idQuestion INT(9),
    reponse VARCHAR(500),
    PRIMARY KEY (idQuestion, idUser)
);


ALTER TABLE QUESTION        ADD FOREIGN KEY (idQuestionnaire)   REFERENCES QUESTIONNAIRE(idQuestionnaire);
ALTER TABLE QUESTION        ADD FOREIGN KEY (idType)            REFERENCES TYPEQUESTION(idType);
ALTER TABLE QUESTIONNAIRE   ADD FOREIGN KEY (idUser)            REFERENCES USERS(idUser);
ALTER TABLE REPONSEUSER     ADD FOREIGN KEY (idUser)            REFERENCES USERS(idUser);
ALTER TABLE REPONSEUSER     ADD FOREIGN KEY (idQuestion)        REFERENCES QUESTION(idQuestion);
ALTER TABLE REPONSEQUESTION ADD FOREIGN KEY (idQuestion)        REFERENCES QUESTION(idQuestion);

INSERT INTO USERS (iduser, prof) VALUES
    (0,true),
    (1,true),
    (2,true),
    (3,false),
    (4,false)
;

INSERT INTO TYPEQUESTION (idType,nomType) VALUES
    (1,'Reponse courte'),
    (2,'Reponse libre'),
    (3, 'truefalse'),
    (4, 'multichoice')
;

