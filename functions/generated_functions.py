def initialize_twitter_api(api_key, api_secret_key, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def initialize_email_client(server_address, server_port, username, password):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Create SMTP session for sending the mail
    session = smtplib.SMTP(server_address, server_port)
    session.starttls() # enable security
    session.login(username, password)
    return session

def compose_email(to_address, subject, body):
    # Create a MIMEText object to represent the email
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Create a message object using MIMEMultipart
    message = MIMEMultipart()
    message['To'] = to_address
    message['Subject'] = subject

    # Attach the email body to the message. It is assumed body is a plain text
    message.attach(MIMEText(body, 'plain'))

    return message

def validate_email_address(email_address):
    # Using a simple regex pattern to validate email address.
    # This pattern can be replaced or modified to suit more specific validation requirements.
    pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    if re.match(pattern, email_address):
        return True
    else:
        return False
    
def send_email(email_obj, email_client):
    """Sends an email object using the given email client.

    Args:
        email_obj: An email object that contains the recipient address, subject, and body.
        email_client: An initialized email client configured to send emails.

    Returns:
        Sends the email and does not return a value.
    """
    try:
        # Use the send_message method of email_client to send the email
        email_client.send_message(email_obj)
        print('Email sent successfully')
    except Exception as e:
        print('Failed to send email:', e)

def generate_result_json(status, message):
    result = { 'status': status, 'message': message }
    return json.dumps(result)