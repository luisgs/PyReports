import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import variables

variables.init()


def emailToConsultant(consultant, listCases):
    # me == my email address
    # consultant == recipient's email address
    print(sys.path)
    me = variables.emailFrom
    consultant = sys.argv[1]

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Please, some of your cases need corrections"
    msg['From'] = me
    msg['To'] = consultant

    # Create the body of the message (a plain-text and an HTML version).
    text = 'Hi!\nHow are you?\nHere is the link you wanted:\n \
        https://www.python.org'
    html = """\
    <html>
    <head></head>
    <body>
        <p>Hi!<br>
        How are you?<br>
        Here is the <a href="https://www.python.org">link</a> you wanted.
        </p>
    </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(variables.SMTPServer)
    s.ehlo()
    s.starttls()
    s.login(variables.emailFrom, variables.password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, consultant, msg.as_string())
    s.quit()
