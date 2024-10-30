from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from datetime import datetime

@bp.route('/')
def index():
    current_year = datetime.now().year
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html', current_year=current_year)

@bp.route('/dashboard')
@login_required
def dashboard():
    current_year = datetime.now().year
    return render_template('dashboard.html', current_year=current_year)

@bp.route('/profile')
@login_required
def profile():
    return render_template('dashboard/profile.html')

@bp.route('/subscription')
@login_required
def subscription():
    return render_template('dashboard/subscription.html')

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    try:
        supabase = get_supabase()
        
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        
        # Prepare update data
        update_data = {
            'username': username,
            'email': email,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # If password change is requested
        if current_password and new_password:
            # Verify current password with Supabase Auth
            try:
                supabase.auth.sign_in_with_password({
                    'email': current_user.email,
                    'password': current_password
                })
                # Update password
                supabase.auth.update_user({'password': new_password})
            except Exception as e:
                flash('Current password is incorrect')
                return redirect(url_for('main.profile'))
        
        # Update user profile in Supabase
        response = supabase.table('users').update(update_data).eq('id', current_user.id).execute()
        
        if response.data:
            flash('Profile updated successfully')
        else:
            flash('Failed to update profile')
            
        return redirect(url_for('main.profile'))
        
    except Exception as e:
        current_app.logger.error(f'Profile update error: {str(e)}')
        flash('An error occurred while updating your profile')
        return redirect(url_for('main.profile'))

