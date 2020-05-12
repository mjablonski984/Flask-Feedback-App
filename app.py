import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail


app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    # in development run in debug mode and set local postgres db -> postgresql://<username>:<password>@<host>/<dbname>
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI_DEV')
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI_PROD')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    source = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, name, email, source, rating, comments):
        self.name = name
        self.email = email
        self.source = source
        self.rating = rating
        self.comments = comments



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        source = request.form['source']
        rating = request.form['rating']
        comments = request.form['comments']
        if name == '' or email == '' or rating == None:
            return render_template('index.html', message='Please enter required fields')
        # check if email already exists in db Feedback table
        if db.session.query(Feedback).filter(Feedback.email == email).count() == 0:    
            data = Feedback(name, email, source, rating, comments)
            db.session.add(data)
            db.session.commit()
            # send mail
            send_mail(name, email, source, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')



if __name__ == '__main__':
    app.run()