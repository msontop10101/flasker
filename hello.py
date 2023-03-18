from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




#Create a flask instance 

app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret Key for Form
app.config['SECRET_KEY'] = 'my supereei10'
#Initialize the database
db = SQLAlchemy(app)

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

#Create A String
def __repr__(self):
    return '<Name %r>' % self.name

#Create a form class
class UserFrom(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    email = StringField('What\'s your email?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NamerForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Create a route decorator
@app.route('/')

def index():
    stuff = "This is a <strong>bold</strong> text"
    fav_pizza = ['pepperoni', 'cheese', 44]
    return render_template('index.html', 
                           stuff=stuff,
                           fav_pizza=fav_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #Validate Form 
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form submitted successfully!')
    return render_template('name.html',
                           name = name,
                           form = form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserFrom()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user == None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User added successfully!')
    our_users=Users.query.order_by(Users.date_added)
    return render_template('add_user.html', 
                           form=form,
                           name=name,
                           our_users=our_users)
#Create custom error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
