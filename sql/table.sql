
USE KAIRO;
DROP TABLE IF EXISTS REPONSEUSER;
DROP TABLE IF EXISTS REPONSEQUESTION;
DROP TABLE IF EXISTS QUESTION;
DROP TABLE IF EXISTS TYPEQUESTION;
DROP TABLE IF EXISTS QUESTIONNAIRE;
DROP TABLE IF EXISTS USERS;



CREATE TABLE USERS(
    idUser VARCHAR(20),
    mdpUser VARCHAR(300),
    prof boolean,
    PRIMARY KEY (idUser)
);


CREATE TABLE QUESTIONNAIRE(
    idQuestionnaire INT(9),
    nom VARCHAR(500),
    info VARCHAR(500),
    idUser VARCHAR(20),
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
    idUser VARCHAR(20),
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
    ('0','a96e0beb59a16b085a7d2b3b5ffd6e5971870aa2903c6df86f26fa908ded2e21',true),
    ('1','288fa5fc4a3b311a79c33edbc8ac0a96e7a4a58235a17216067f31dfe6d52a36',true),
    ('2','ead312b5d9795fee67deb9b6251732cffab8f6daa93edb10805fe0bbfb620371',true),
    ('3','aea2e1dc358f372eaa233677962de08214dd2784c976a19cee7e2f9c4dc6203e',false),
    ('4','8e550653d0f22337638dc1a6da6d5ec54271ff7eee3cf72cc9009ae08aed600c',false)
;

INSERT INTO TYPEQUESTION (idType,nomType) VALUES
    (1,'Reponse courte'),
    (2, 'truefalse'),
    (3, 'multichoice')
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

