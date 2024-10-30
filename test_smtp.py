import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket
import ssl

# Gmail SMTP settings for testing
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "your.email@gmail.com"  # Replace with your Gmail
smtp_password = "your-app-password"     # Replace with Gmail App Password

def test_smtp():
    try:
        print(f"Testing connection to {smtp_server}:{smtp_port}...")
        
        # Create SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.set_debuglevel(2)
        
        print("Connected to server")
        
        # Start TLS
        print("Starting TLS...")
        server.starttls()
        print("TLS started")
        
        # Login
        print("Attempting login...")
        server.login(smtp_username, smtp_password)
        print("Login successful")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = "ojoseph@mac.com"
        msg['Subject'] = "SMTP Test"
        body = "This is a test email from Python"
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print("Sending email...")
        server.send_message(msg)
        print("Email sent successfully!")
        
        server.quit()
        
    except socket.timeout:
        print("Connection timed out - server may be blocking connections")
    except socket.gaierror:
        print("DNS lookup failed - check server hostname")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed - check username and password")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        if 'server' in locals():
            server.quit()

if __name__ == "__main__":
    test_smtp() 