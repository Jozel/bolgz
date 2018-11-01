from flask import Flask, request, redirect, render_template,session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "super secret key"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body ):
        self.title = title
        self.body = body
        self.owner = owner
        if pub_date is None:
         pub_date = datetime.utcnow()
        self.pub_date = pub_dat

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(130), unique=True)
    password = db.Column(db.String(130))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pasword = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        exist = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return "<h1>Duplicate user</h1>"

        if len(username) > 3 and len(password) > 3 and password == verify and not exist:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('signup.html',
            username=username,
            username_error=username_error,
            password_error=password_error,
            verify_error=verify_error
            )

    return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    username_error = ""
    password_error = ""

    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            return redirect('/newpost')
        if not user:
            return render_template('login.html', username_error="Username does not exist.")
        else:
            return render_template('login.html', password_error="Your username or password was incorrect.")

    return render_template('login.html')   

@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(username=username['username']).first()

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('userid')
    posts = Blog.query.order_by(Blog.pub_date.desc())

    if blog_id:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", title=post.title, body=post.body, user=post.owner.username, pub_date=post.pub_date, user_id=post.owner_id)
    if user_id:
        entries = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('user.html', entries=entries)

    return render_template('blog.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    form = BlogForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('newpost.html', form=form)
        else:

            owner = User.query.filter_by(username=session['username']).first()
            blog_title = form.blog_title.data
            blog_post = form.blog_post.data

            new_blog = Blog(blog_title, blog_post, owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect(url_for('blog', id=new_blog.id))

    return render_template('newpost.html', form=form, title="Add a Blog Entry")


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

  

 #@app.route('/', methods=['GET', 'POST'])
#def new_entry():
    

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        print(body)
        new_entry = Blog(title, body) 
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/blog')
    
    return render_template('new_entry.html')

#@app.route('/blog', methods=['GET'])
#def blog():
 #    blog_id = request.args.get('id')
  #   return render_template('main_blog.html', blog=blog)
    # if blog_id:
        #blog_id = request.args.get('id')
       # blog = Blog.query.get(blog_id)

    

if __name__ == '__main__':
    app.run()