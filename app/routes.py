from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

import random
from urllib.parse import unquote

from app import app, db
from config import Config

from app.forms import GratefulForm, LoginForm, RegistrationForm, EmptyForm
from app import models

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    # New Post
    form = GratefulForm()
    placeholders = random.sample(app.config['PLACEHOLDERS'], 3)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            models.create_post(current_user, [form.item1.data, form.item2.data, form.item3.data])
        else:
            print("not authenticated")
            post_url = url_for('post', item1=form.item1.data, item2=form.item2.data, item3=form.item3.data)
            # TODO: Make post after registration
            return redirect(url_for('register', next=post_url))
    
    # Feed
    feed = None
    if current_user.is_authenticated:
        feed = current_user.followed_posts()

    
    return render_template('index.html', grateful_form=form, placeholders=placeholders, feed=feed)


@app.route('/@<handle>')
def profile(handle):
    profile_user = models.User.query.filter_by(handle=handle).first_or_404(description=f"User @{handle} doesn't exist")
    return render_template('profile.html', user=profile_user, form=EmptyForm())


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post(item1, item2, item3):
    models.create_post(current_user, item1, item2, item3)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.create_user(form.handle.data, form.email.data, form.password.data)
        login_user(user, remember=False)
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid handle or password')
            return redirect(url_for('login'))
        print("logging in, remember =",form.remember_me.data)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/settings')
@login_required
def settings():
    flash("Settings not yet implemented")
    return redirect(url_for('index'))


@app.route('/follow/<handle>', methods=['POST'])
@login_required
def follow(handle):
    form = EmptyForm()
    if form.validate_on_submit():
        print("Form validated")
        user = models.User.query.filter_by(handle=handle).first()
        if user is None:
            flash('User {} not found.'.format(handle))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('profile', handle=handle))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(handle))
        return redirect(url_for('profile', handle=handle))
    else:
        print("form not validated")
        return redirect(url_for('index'))


@app.route('/unfollow/<handle>', methods=['POST'])
@login_required
def unfollow(handle):
    form = EmptyForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(handle=handle).first()
        if user is None:
            flash('User {} not found.'.format(handle))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('profile', handle=handle))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(handle))
        return redirect(url_for('profile', handle=handle))
    else:
        return redirect(url_for('index'))







