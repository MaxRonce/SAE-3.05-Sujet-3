from hashlib import sha256

from link_front_back import db_link
from .app import app, db


@app.cli.command()
def hashP():
    users = db_link.ses.query(db_link.User).all()
    for u in users:
        salted_password = str(u.idUser) + u.mdpUser
        u.mdpUser = sha256(salted_password.encode()).hexdigest()
    db_link.ses.commit()
    print("Done")


