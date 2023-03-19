from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash



#Create a flask instance 

app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret Key for Form
app.config['SECRET_KEY'] = 'my supereei10'
#Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)



#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Password workings
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is nomett a readable attr!')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)
    
#Create a blog post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))

#Create A String
def __repr__(self):
    return '<Name %r>' % self.name

#Create a form class
class UserFrom(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='password must match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Create Post From class
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Blog post route 
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        #Clear form 
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        #Add post to database
        db.session.add(post)
        db.session.commit()
        flash('Post successfully added!')
    return render_template('add_post.html',
                           form=form)

#Posts Route
@app.route('/posts')
def posts():
    posts = Post.query.order_by(Post.date_posted)
    return render_template('posts.html', posts=posts)

#Individual blog post
@app.route('/posts/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

#Edit blog post 
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash('Post has been updated!')
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html',
                           form=form,
                           post=post)

    


#Update database record
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserFrom()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try: 
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template('update.html',
                                   form = form,
                                   name_to_update = name_to_update)
        except:
            flash('Error Occured!')
            return render_template('update.html',
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template('update.html',
                                   form = form,
                                   name_to_update = name_to_update)

#Delete record from databse 
@app.route('/delete/<int:id>', methods=['GET','POST','DELETE'])
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserFrom()
    try: 
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully!')
        our_users=Users.query.order_by(Users.date_added)
        return render_template('add_user.html', 
                           form=form,
                           name=name,
                           our_users=our_users)
    except:
        flash('Error Occured!')
        our_users=Users.query.order_by(Users.date_added)
        return render_template('add_user.html', 
                           form=form,
                           name=name,
                           our_users=our_users)


class NamerForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PasswordForm(FlaskForm):
    email = StringField('Enter your email', validators=[DataRequired()])
    password = PasswordField('Enter your password', validators=[DataRequired()])
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


@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    password_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        #Look up the user
        password_to_check = Users.query.filter_by(email=email).first()
        #Check password
        passed = check_password_hash(password_to_check.password_hash,password)

        form.email.data = ''
        form.password.data = ''
    return render_template('test_pw.html',
                           email = email,
                           password = password,
                           password_to_check = password_to_check,
                           passed = passed,
                           form = form)

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
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
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
