# SAE-3.05-Sujet-3
SAE-3.05-Sujet-3 EQUIPE : Louise CHABIN, Louis NOEL, Antonin REYDET, Maxime RONCERAY


# But de l’application :
Permettre aux enseignants de gérer des questionnaires et des questions pour être</br>
utilisées dans les outils Moodle ou auto-multiple-choice.</br>
### Explication</br>
Moodle est le LMS le plus utilisé au monde et connaît différents formats de questions dont</br>
le format GIFT et le format XML qui permettent de représenter différents types de</br>
questions.
Le logiciel auto-multiple-choice permet quand à lui de proposer des QCM au format papier
avec un format un peu plus simple et limité de questions.</br>
### Fonctionnement souhaité : </br>
- Le logiciel devra permettre de créer des questions de différentes natures :</br>
- questions à choix multiples</br>
- questions à réponse courte (texte ou numérique)</br>

Il devra aussi proposer une fonctionnalité d’utiliser un programme en Python ou</br>
JavaScript pour générer des familles de questions avec du contenu numérique qui</br>
auront des contenus individualisés (valeurs numériques ou autres différentes)</br>

### Liens :

- Drive : https://drive.google.com/drive/u/0/folders/1gAIm-eTTWUM5OioAYPuapIa_z06Ucecf </br>
- Trello : https://trello.com/w/sae305sujet3 </br>
- Figma : https://www.figma.com/team_invite/redeem/H4xrpIno8YTb91kIYF7qP5


### Manuel d'installation :
- Installer MySQL 8.0.26 https://dev.mysql.com/downloads/mysql/
- Installer Python 3.9.7 https://www.python.org/downloads/release/python-397/
- Dans le fichier ```setupdb.py``` modifier les lignes suivante avec vos informations de connexion
```python
login, passwd, serveur, bd = "root", "ronceray", "localhost", "kairo"
engine = create_engine('mysql+mysqldb://' + login + ':' + passwd + '@' + serveur + '/' + bd)
```
- Executez le fichier ```table.sql``` dans votre base de données
- (Optionel) utilisez la commande ````flask hashp```` afin de configurer les utilisateurs par défaut dans votre database
- Utilisez la commande ```flask run``` pour lancer le serveur
- Si vous ne souhaitez pas utiliser les utilisateurs par défaut, vous pouvez vous inscrire sur le site


#### REQUIREMENTS
- click==8.1.3</br>
- Flask==2.2.2</br>
- Flask-Login==0.6.2</br>
- Flask-MySQLdb==1.0.1</br>
- Flask-SQLAlchemy==3.0.2</br>
- Flask-WTF==1.0.1</br>
- greenlet==2.0.1</br>
- itsdangerous==2.1.2</br>
- Jinja2==3.1.2</br>
- MarkupSafe==2.1.1</br>
- mysqlclient==2.1.1</br>
- python-dotenv==0.21.0</br>
- SQLAlchemy==1.4.45</br>
- Werkzeug==2.2.2</br>
- WTForms==3.0.1</br>
