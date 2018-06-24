from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm, RegisterForm
from flask_login import login_user,login_required,logout_user
from ..models import User
from .. import db

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalida User')
        flash(user.verify_password(form.password.data))
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are lougout')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can login now')
        return redirect(url_for('.login'))
    return render_template('auth/register.html',form=form)



