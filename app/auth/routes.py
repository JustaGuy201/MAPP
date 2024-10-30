from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.models import User
from app.supabase_client import get_supabase
from app.utils.email import send_confirmation_email

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            supabase = get_supabase()
            
            auth_response = supabase.auth.sign_up({
                'email': email,
                'password': password
            })
            
            if hasattr(auth_response, 'user') and auth_response.user:
                user_data = {
                    'id': auth_response.user.id,
                    'email': email,
                    'username': username,
                    'is_active': True,
                    'subscription_type': 'free'
                }
                
                db_response = supabase.table('users').insert(user_data).execute()
                
                if db_response.data:
                    # Send confirmation email
                    if send_confirmation_email(email, username):
                        flash('Registration successful! Please check your email.')
                    else:
                        flash('Registration successful, but confirmation email failed to send.')
                    return redirect(url_for('auth.login'))
                    
        except Exception as e:
            flash(f'Registration failed: {str(e)}')
            
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            supabase = get_supabase()
            response = supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            
            if hasattr(response, 'user') and response.user:
                user = User.get_by_email(email)
                if user:
                    login_user(user)
                    return redirect(url_for('main.dashboard'))
                else:
                    flash('User not found in database.')
            else:
                flash('Invalid email or password.')
                
        except Exception as e:
            flash(f'Login failed: {str(e)}')
            
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))