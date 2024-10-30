from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

def send_confirmation_email(to_email, username):
    try:
        message = Mail(
            from_email='artist@justaguysmusic.com',
            to_emails=to_email,
            subject='Welcome to MAPP - Account Confirmation',
            html_content=f'''
            <h2>Welcome to MAPP!</h2>
            <p>Hi {username},</p>
            <p>Thank you for signing up. Your account has been created successfully.</p>
            <p><strong>Username:</strong> {username}<br>
            <strong>Email:</strong> {to_email}</p>
            <p>You can now log in and start using MAPP!</p>
            <p>Best regards,<br>The MAPP Team</p>
            ''')
        
        sg = SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        
        current_app.logger.info(f"SendGrid Response: {response.status_code}")
        return response.status_code == 202
            
    except Exception as e:
        current_app.logger.error(f"Email sending error: {str(e)}")
        return False 