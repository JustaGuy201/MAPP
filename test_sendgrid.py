import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def test_sendgrid():
    message = Mail(
        from_email='artist@justaguysmusic.com',
        to_emails='ojoseph@mac.com',
        subject='Testing SendGrid',
        html_content='<strong>This is a test email from SendGrid</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.body}")
        print(f"Response Headers: {response.headers}")
        return "Email sent successfully!"
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

if __name__ == "__main__":
    test_sendgrid() 