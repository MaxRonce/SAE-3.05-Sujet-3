from hashlib import sha256

from link_front_back import db_link
from .app import app, db


@app.cli.command()
def hashP():
    users = db_link.ses.query(db_link.User).all()
    for u in users:
        u.mdpUser = sha256(u.mdpUser.encode('utf-8'))
    db_link.ses.commit()
    print("Done")
