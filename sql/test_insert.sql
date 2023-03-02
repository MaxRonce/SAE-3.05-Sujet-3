USE KAIRO;
INSERT INTO USERS (iduser, prof) VALUES
    (0,true),
    (1,true),
    (2,true),
    (3,false),
    (4,false)
;


INSERT INTO QUESTIONNAIRE (idQuestionnaire, nom, info, idUser) VALUES
    (1,'Mathématiques','addition et soustraction',2),
    (2,'Français','conjugaison',2),
    (3,'Anglais','mot simple',1);



INSERT INTO TYPEQUESTION (idType,nomType) VALUES
    (1,'Reponse courte'),
    (2,'Reponse libre'),
    (3, 'truefalse'),
    (4, 'multichoice')
;


INSERT INTO QUESTION (idquestion, question, template, valeurPoint, pointNegatif, idquestionnaire, idType) VALUES

    (20,'2+2',false,4,true,1,1),
    (21,'le verbe être au present à la premiere personne du singulier',false,10,true,2,1),
    (22,'que signifie : hello world',false,5,false,3,2),
    (23,'35*156',false, 2, false, 1,1),
    (24,'le verbe manger au present a la deuxieme personne du pluriel',false,10,true,2,1),
    (25,'que signifie le mot : improve',false,2,true,3,1)
;


INSERT INTO REPONSEQUESTION (idReponse, reponse, idQuestion) VALUES
    (40,'artichaud',20),
    (41,'4',20),
    (42,'je suis',21),
    (43,'suis',21),
    (44,'sommes',21),
    (45,'hello le monde',22),
    (46,'bonjour monde',22),
    (47,'5460',23),
    (48,'546',23),
    (49,'vous mangez',24),
    (50,'vous manger',24),
    (51,'mangez',24),
    (52,'impovisation',25),
    (53,'améliorer',25)
;


INSERT INTO REPONSEUSER (iduser, idQuestion, reponse) VALUES
    (33,20,''),
    (33,23,''),
    (33,21,''),
    (33,24,''),
    (33,22,''),
    (33,25,''),
    (34,20,''),
    (34,23,''),
    (34,21,''),
    (34,24,''),
    (34,22,''),
    (34,25,'')
;
