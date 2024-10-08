import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
# Load environment variables from .env file
load_dotenv()


smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")


# Load the Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))

# Load the HTML email template
template = env.get_template('email_template.html')


def send_email(subject, message, email, name, channel_name):
    # Define dynamic content
    context = {
        'subject': subject,
        'name':name,
        'channel_name': channel_name,
        'message': message
    }

    # Render the template with dynamic content
    html_content = template.render(context)


    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = "channelsync@notify.com"
    msg['To'] = email

    print(html_content)

    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # Send email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail("channelsync@notify.com", email, msg.as_string())
    server.quit()
