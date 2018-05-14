from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_cors import CORS
from lepl.apps.rfc3696 import Email


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)
heroku = Heroku(app)
db = SQLAlchemy(app)


# Create our database model
class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(15), unique=True)
    msg = db.Column(db.String(500), unique=True)

    def __init__(self, name, email, phone, msg):
        self.name = name
        self.email = email
        self.phone = phone
        self.msg = msg

    def __repr__(self):
        return '<email %r>, <name %r>, <phone %r>, <msg %r>' % self.email % self.name % self.phone % self.msg


# Save e-mail to database and send to success json
@app.route('/add', methods=['POST'])
def add_email():
    if request.method == 'POST':
        email_validator = Email()
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['msg']
        if email_validator(email):
            # Check that email does not already exist (not a great query, but works)
            if not db.session.query(Contact).filter(Contact.email == email).count():
                c = Contact(name, email, phone, msg)
                db.session.add(c)
                db.session.commit()
                return jsonify({"status": True})
    return jsonify({"status": False})


# Save e-mail to database and send to success json
@app.route('/remove', methods=['POST'])
def remove_email():
    if request.method == 'POST':
        email_validator = Email()
        email = request.form['email']
        if email_validator(email):
            # Check that email does already exist
            c = db.session.query(Contact).filter(Contact.email == email)
            if c:
                db.session.delete(c)
                db.session.commit()
                return jsonify({"status": True})
    return jsonify({"status": False})


@app.route('/', defaults={'path': ''}, methods=[
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
@app.route('/<path:path>', methods=[
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
def index(path):
    return redirect("https://virtualskin-project.github.io")


if __name__ == '__main__':
    app.debug = False
    app.run()
    db.create_all()
