from flask_login import LoginManager
from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)
login_manager = LoginManager(app)


app.config['SECRET_KEY'] = b'4004789735821215b5f69ce64a39ed41874ed260b8da7b4720e70d047db6447a'
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''

db = MySQL(app)

app.config['UPLOAD_FOLDER'] = 'static/uploaded_files'

ALLOWED_EXTENSIONS = {'xml'}


if __name__ == "__main__":
    app.run()
