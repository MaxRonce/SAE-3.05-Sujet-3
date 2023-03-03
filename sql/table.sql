
USE KAIRO;
DROP TABLE IF EXISTS REPONSEUSER;
DROP TABLE IF EXISTS REPONSEQUESTION;
DROP TABLE IF EXISTS QUESTION;
DROP TABLE IF EXISTS TYPEQUESTION;
DROP TABLE IF EXISTS QUESTIONNAIRE;
DROP TABLE IF EXISTS USERS;



CREATE TABLE USERS(
    idUser INT(9),
    mdpUser VARCHAR(300),
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
    essaiNumero INT(9),
    reponse VARCHAR(500),
    PRIMARY KEY (idQuestion, idUser, essaiNumero)
);

ALTER TABLE QUESTION        ADD FOREIGN KEY (idQuestionnaire)   REFERENCES QUESTIONNAIRE(idQuestionnaire);
ALTER TABLE QUESTION        ADD FOREIGN KEY (idType)            REFERENCES TYPEQUESTION(idType);
ALTER TABLE QUESTIONNAIRE   ADD FOREIGN KEY (idUser)            REFERENCES USERS(idUser);
ALTER TABLE REPONSEUSER     ADD FOREIGN KEY (idUser)            REFERENCES USERS(idUser);
ALTER TABLE REPONSEUSER     ADD FOREIGN KEY (idQuestion)        REFERENCES QUESTION(idQuestion);
ALTER TABLE REPONSEQUESTION ADD FOREIGN KEY (idQuestion)        REFERENCES QUESTION(idQuestion);

INSERT INTO USERS (iduser,mdpUser, prof) VALUES
    (0,'test',true),
    (1,'test',true),
    (2,'test',true),
    (3,'test',false),
    (4,'test',false)
;

INSERT INTO TYPEQUESTION (idType,nomType) VALUES
    (1,'Reponse courte'),
    (2,'Reponse libre'),
    (3, 'truefalse'),
    (4, 'multichoice')
;


INSERT INTO QUESTIONNAIRE (idQuestionnaire, nom, info, idUser) VALUES
    (1,'Mathématiques','addition et soustraction',2),
    (2,'Français','conjugaison',2),
    (3,'Anglais','mot simple',1)
;


-- CREATE TRIGGER trg_check_duplicate_questionnaire BEFORE INSERT ON QUESTIONNAIRE
-- FOR EACH ROW
-- BEGIN
--     DECLARE count INT;
--     SELECT COUNT(*) INTO count FROM QUESTIONNAIRE WHERE nom = NEW.nom;
--     IF count > 0 THEN
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A questionnaire with the same name already exists';
--     END IF;
-- END;

