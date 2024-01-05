import imaplib
import email
import requests

# Email server credentials and settings
imap_url = 'imap.example.com'
username = ''
password = ''
mailbox = 'INBOX'

# Connect to the email server
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(username, password)
mail.select(mailbox)

# Search for emails
status, messages = mail.search(None, 'ALL')
messages = messages[0].split()

for mail_id in messages:
    # Fetch each email
    _, msg_data = mail.fetch(mail_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            email_subject = msg['subject']
            email_from = msg['from']
            email_body = msg.get_payload(decode=True).decode()

            # Send email content to Flask API
            response = requests.post('http://localhost:5000/predict', data={'text': email_body})
            if response.status_code == 200:
                # If the email is classified as spam, take an action
                if response.json()['spam']:
                    print(f"Spam detected in email {email_subject} from {email_from}")

# Close the connection
mail.close()
mail.logout()
