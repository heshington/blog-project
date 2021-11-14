from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime

## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'full'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField('Blog Content', validators=[DataRequired()])
    submit = SubmitField("Submit Post", )


posts = db.session.query(BlogPost).all()


@app.route('/')
def get_all_posts():
    all_posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=all_posts)


@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    if request.method == "GET":
        form = CreatePostForm()
        return render_template("make-post.html", form=form)
    elif request.method == "POST":
        now_date = datetime.datetime.now()
        formatted_date = now_date.strftime("%B %d, %Y")
        new_blog = BlogPost(
            title=request.form.get('title'),
            subtitle=request.form.get('subtitle'),
            date=formatted_date,
            body=request.form.get('body'),
            author=request.form.get('author'),
            img_url=request.form.get('img_url')
        )
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('get_all_posts'))


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        print(blog_post.id)
        print(index)
        print(requested_post)
        if blog_post.id == index:
            requested_post = blog_post

    return render_template("post.html", post=requested_post)

@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    return render_template("make-post.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
