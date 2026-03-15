from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html', user=current_user)

@main_bp.route('/test')
def test():
    try:
        return '<h1>Flask OK! Templates: ' + str(os.listdir('templates'))
    except Exception as e:
        return f'Error: {str(e)}', 500
