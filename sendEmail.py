#!/usr/bin/env python3

import smtplib
import variables
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# me == my email address
# you == recipient's email address
me = variables.emailFrom
consultant = sys.argv[1]

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Please, some of your cases need corrections"
msg['From'] = me
msg['To'] = consultant

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
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

def foo():
    return 1

if __name__ == '__main__':
    foo()
