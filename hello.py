from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



#Create a flask instance 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my supereei10'

#Create a form class
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

#Create custom error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
