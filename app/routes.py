from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from flask_mail import Message
from app import mail

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html', user=current_user)

@bp.route('/profile')
@login_required
def profile():
    return render_template('dashboard/profile.html', user=current_user)

@bp.route('/test-email')
def test_email():
    try:
        msg = Message('Test Email from MAPP',
                     sender=current_app.config['MAIL_DEFAULT_SENDER'],
                     recipients=['ojoseph@mac.com'])  # Replace with your email
        msg.body = 'This is a test email from your MAPP application.'
        mail.send(msg)
        return 'Email sent! Please check your inbox.'
    except Exception as e:
        return f'Error sending email: {str(e)}'