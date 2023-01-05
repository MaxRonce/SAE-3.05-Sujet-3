INSERT INTO USERS (iduser, prof) VALUES
    (0,true),
    (1,true),
    (2,true),
    (3,false),
    (4,false)
;


INSERT INTO QUESTIONNAIRE (idQuestionnaire, nom, descr, idUser) VALUES
    (1,'Mathématiques','addition et soustraction',30),
    (2,'Français','conjugaison',32),
    (3,'Anglais','mot simple',31)
;


INSERT INTO TYPEQUESTION (idType,nomType) VALUES
    (1,'Reponse courte'),
    (2,'Reponse libre'),
    (3, 'truefalse'),
    (4, 'multichoice')
;


INSERT INTO QUESTION (idquestion, question, template, valeurPoint, pointNegatif, idquestionnaire, idType) VALUES
    (20,'2+2',NONE,4,true,1,11),
    (21,'le verbe être au present à la premiere personne du singulier',NONE,10,true,2,12),
    (22,'que signifie : hello world',NONE,5,false,3,13),
    (23,'35*156',NONE, 2, false, 1,11),
    (24,'le verbe manger au present a la deuxieme personne du pluriel',NONE,10,true,2,12),
    (25,'que signifie le mot : improve',NONE,2,true,3,12)
;


INSERT INTO REPONSEQUESTION (idReponse, reponse, valide, idQuestion) VALUES
    (40,'artichaud',false,20),
    (41,'4',true,20),
    (42,'je suis',true,21),
    (43,'suis',true,21),
    (44,'sommes',false,21),
    (45,'hello le monde',false,22),
    (46,'bonjour monde',true,22),
    (47,'5460',true,23),
    (48,'546',false,23),
    (49,'vous mangez',true,24),
    (50,'vous manger',false,24),
    (51,'mangez',true,24),
    (52,'impovisation',false,25),
    (53,'améliorer',true,25)
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
