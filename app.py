"""Blogly application."""
from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "speakcatacean"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    tags = Tag.query.all()
    return render_template("posts/homepage.html", posts=posts, tags=tags)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


# /////////////////////////////////////////////////////////
# users routes

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users=users)


@app.route('/users/new')
def show_add_form():
    """Show form to add a new user"""
    return render_template('users/add_user.html')


@app.route('/users/new', methods=["POST"])
def add_new_user():
    """Add new user to database"""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['img-url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} added.")
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_profile(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Show form to edit user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit_profile.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Update user in db"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["img-url"]

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes user and redirects back to users list"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# //////////////////////////////////////////////////////////////////////////////////
# posts routes

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def show_post_form(user_id):
    """Show form to make new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_post(user_id):
    """Add post to db"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(tag_id) for tag_id in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'], content=request.form['content'], user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>', methods=["GET"])
def show_post_details(post_id):
    """Show post details"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template('posts/show_post.html', user=user, post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_edit_post_form(post_id):
    """Show edit post form"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/posts/edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Update post in db"""
    post = Post.query.get_or_404(post_id)
    tag_ids = [int(tag_id) for tag_id in request.form.getlist("tags")]

    post.title = request.form['title']
    post.content = request.form['content']
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post update db"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")


# //////////////////////////////////////////////////////////////////////////////////
# tagss routes

@app.route('/tags')
def list_all_tags():
    """List all tags"""
    tags = Tag.query.all()
    return render_template('tags/list_tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show tag details"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag_details.html', tag=tag)


@app.route('/tags/new', methods=["GET"])
def show_tag_form():
    """Show form to add new tag"""
    return render_template('tags/create_tag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Add tag to db"""
    tag = Tag(name=request.form["name"])

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_edit_tag_form(tag_id):
    """Show form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    """Update tag in db"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag_id}")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete tag and update db"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')