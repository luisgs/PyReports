import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import variables

# We bring into our lib global variables such as passwords, emails...
variables.init()


def listConsulCases(dictCases):
    htmlCases = ""
    href = 'https://hp.my.salesforce.com/_ui/search/ui/UnifiedSearchResults?searchType=2&sen=500&sen=00O&str='
    for case in dictCases:
        # <a href="http://www.yahoo.com">here</a>
        listErrors = [('<dd>- %s </dd><br>' %
                       (Error)) for Error in dictCases[case]]
        htmlCases = ('%s<dl><dt><a href=\"%s%s\">%s</a>:</dt><br>%s' %
                     (htmlCases, href, str(case),
                      str(case), "".join(listErrors)))
    return "%s</dt>" % (htmlCases)


def emailToConsultant(employee, email, listCases):
    # me == my email address
    # consultant == recipient's email address
    me = variables.emailFrom
    consultant = employee

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Please, some of your cases need corrections"
    msg['From'] = me
    msg['To'] = consultant
    msg['Cc'] = ""
    msg['Bc'] = ""

    # Create the body of the message (a plain-text and an HTML version).
    text = 'Hi!\nHow are you?\nWe need you to correct some cases\n\n \
        Please open a html version that has been sent with this email for \
        further details'
    html = """\
<html>
<head></head>
<body>

    <p>Hi %s!<br> <br>

    How are you?<br>
    We need you to correct these cases below: <br>
    %s
    </p>
Thank you!
</body>
</html>
    """ % (employee.partition(' ')[0], listConsulCases(listCases))
    print(html)
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


def sendEmailToConsultants(ListOfErrors):
    emailToConsultant(ListOfErrors[0][0], "luis.ild@gmail.com",ListOfErrors[0][2])
#    [emailToConsultant(consultantReport[0],
#                       consultantReport[1],
#                       consultantReport[2]) for consultantReport in ListOfErrors]
