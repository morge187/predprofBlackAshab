from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from wtf_forms.auth_forms import RegisterForm
from models.user import User
from app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users')
@login_required
def users():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('main.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username exists')
            return render_template('admin/create_user.html', form=form)
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role='user'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)
