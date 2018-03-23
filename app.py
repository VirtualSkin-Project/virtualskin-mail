from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)

heroku = Heroku(app)
db = SQLAlchemy(app)


# Create our database model
class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<email %r>' % self.email


# Save e-mail to database and send to success json
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(Contact).filter(Contact.email == email).count():
            c = Contact(email)
            db.session.add(c)
            db.session.commit()
            return {"status": True}
    return {"status": False}


# Save e-mail to database and send to success json
@app.route('/remove', methods=['POST'])
def remove():
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does already exist
        if db.session.query(Contact).filter(Contact.email == email).count():
            c = Contact(email)
            db.session.delete(c)
            db.session.commit()
            return {"status": True}
    return {"status": False}


if __name__ == '__main__':
    app.debug = False
    app.run()
    db.create_all()
