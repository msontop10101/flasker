from flask import Flask, render_template

#Create a flask instance 

app = Flask(__name__)

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

#Create custom error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500