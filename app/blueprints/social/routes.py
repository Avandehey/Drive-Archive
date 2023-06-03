from flask import render_template, flash, redirect, url_for, g
from flask_login import current_user, login_required
from . import bp

from app.models import Post, User
from app.forms import PostForm

@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    
    # If the form is submitted and passes validation
    if form.validate_on_submit():
        p = Post(body=form.body.data)
        p.user_id = current_user.user_id
        p.commit()
        flash('Published', 'success')
        return redirect(url_for('social.user_page', username=current_user.username))
    
    # Render the post.jinja template with the form and user_search_form
    return render_template('post.jinja', form=form, user_search_form=g.user_search_form)

@bp.route('/userpage/<username>')
@login_required
def user_page(username):
    # Query the User model for a user with the given username
    user = User.query.filter_by(username=username).first()
    
    # Render the user_page.jinja template with the title, user, and user_search_form
    return render_template('user_page.jinja', title=username, user=user, user_search_form=g.user_search_form)

@bp.post('/user-search')
@login_required
def user_search():
    # If the user_search_form is submitted and passes validation
    if g.user_search_form.validate_on_submit():
        # Redirect to the user_page route with the username from the user_search_form
        return redirect(url_for('social.user_page', username=g.user_search_form.user.data))
    
    # Redirect to the main.home route
    return redirect(url_for('main.home'))