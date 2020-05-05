from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from website import db
from website.models import Post
from website.posts.forms import PostForm

# creating a blueprint for posts package
posts = Blueprint('posts', __name__)

# all routes will all assign a header string through Jinja variables to the respective html file so
# it can be used as the header for each page


# Generates a form for creating a new post and valid posts are sent to database table Post
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('Post/create_post.html', header='Create Your Post',
                           form=form, legend='New Post')


# generates an update form for a specific queried post from the database and a new page for a user who
# wants to update a post, only user that has made the post can access this page and any other user who
# tries inputting a link for a post that is not theirs will be met with a 404 page not found error
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('users.user_posts', username=current_user.username))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('Post/create_post.html', header='Update Post',
                           form=form, legend='Update Post')


# if user has chosen to delete a post, he will be met by this route which deletes that post forever from
# the database and send a success message and redirects to the home page, once again, only user that has
# made the post can access this page and any other user who tries inputting a link for deleting a post
# that is not theirs will be met with a 404 page not found error
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))


# queries all posts from database and displays 5 per page
@posts.route("/all_posts")
@login_required
def all_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('Post/all_posts.html', posts=posts, header="All Posts")

