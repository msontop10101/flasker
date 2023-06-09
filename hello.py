from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, UserFrom, PostForm, NamerForm, PasswordForm, SearchForm
from flask_ckeditor import CKEditor



convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}





#Create a flask instance 

app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret Key for Form
app.config['SECRET_KEY'] = 'my supereei10'
#Initialize the database
# db = SQLAlchemy(app)
ckeditor = CKEditor(app)

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app,db,render_as_batch=True)

#Flask Login Moves 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#Pass Stuff to Navgar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

#Create search Function
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        #Get Data from submitted form
        post.searched = form.searched.data
        #Query the database 
        return render_template('search.html',
                               form=form,
                               searched = post.searched) 

#Create Login 
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Successful')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password!')
        else:
            flash('User doesn\'t exist!')
    return render_template('login.html', form=form)

#Create Logout page
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You\'ve been logged out!')
    return redirect(url_for('login'))


#Create Dashboard 
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

#Admin Page
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


    
#Create a blog post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    #Foreign key refering to the primary key of the user
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(500), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Password workings
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='poster')

    @property
    def password(self):
        raise AttributeError('Password is nomett a readable attr!')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

#Create A String
def __repr__(self):
    return '<Name %r>' % self.name




#Blog post route 
@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Post(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
        #Clear form 
        form.title.data = ''
        form.content.data = ''
        # form.author.data = ''
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
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash('Post has been updated!')
        return redirect(url_for('post', id=post.id))
    if current_user.id == post.poster_id:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html',
                               form=form,
                               post=post)
    else:
        posts = Post.query.order_by(Post.date_posted)
        return render_template('posts.html', posts=posts)

#Delete blog post 
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Post was successfully deleted')
            posts = Post.query.order_by(Post.date_posted)
            return render_template('posts.html', posts=posts)
        except:
            flash('Error Occured!')
            posts = Post.query.order_by(Post.date_posted)
            return render_template('posts.html', posts=posts)
    else:
        posts = Post.query.order_by(Post.date_posted)
        return render_template('posts.html', posts=posts)



#Update database record
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserFrom()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']
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
@login_required
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserFrom()
    if current_user.id == id:
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
    else:
        flash('Sorry you can\'t delete this user!')
        our_users=Users.query.order_by(Users.date_added)
        return render_template('add_user.html', 
                           form=form,
                           name=name,
                           our_users=our_users)


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
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
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
