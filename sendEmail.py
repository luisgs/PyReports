import sys
import functions
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import variables
import globalVariables


# We bring into our lib global variables such as passwords, emails...
variables.init()


def listConsulCases(ListCases):
    listErrors = ""
    href = 'https://hp.my.salesforce.com/_ui/search/ui/UnifiedSearchResults?searchType=2&sen=500&sen=00O&str='
    htmlCases="<ul><ol>"
    for case in ListCases:	#-> case, [ErrorDescription!]
        htmlCases += ('<li><a href=\"%s%s\">%s</a>:</li><ul>' %
                     (href, str(case), str(case)))
        for Error in ListCases[case]:
            htmlCases += ('<li>%s</li>' % str(Error))

        htmlCases += ('</ul>')
	
    return htmlCases+"</ol></ul>"


def emailToConsultant(employee, email, listCases):
    # consultant == recipient's email address

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Some of your cases need corrections. Please, fix them!"
    msg['From'] = variables.emailFrom 
    msg['To'] = email

    # Create the body of the message (a plain-text and an HTML version).
    text = 'Hi!\nHow are you?\nWe need you to correct some cases\n\n \
        Please open a html version that has been sent with this email for \
        further details'
    html = """\
<html>
<head></head>
<body>

Hi %s!<br> <br>

How are you?<br>
We need you to correct these cases below: <br>

<p style="text-indent: 5em;">
%s
</p>
    
Thank you!
</body>
</html>""" % (employee.partition(' ')[0], listConsulCases(listCases))
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    functions.sendEmail(msg['From'], msg['To'], msg.as_string(), variables.SMTPServer)
#    print(html)


def emailToBoss(boss, email, AllConsultantsCases):
    # We will send to boss (name)'s email a list with ALL his employess cases that need action.
    # Dear boss,
    # your consulants did these errors:
    # - Luis: Case 123: wrong ID...

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Complete list of cases that need action!"
    msg['From'] = variables.emailFrom 
    msg['To'] = email

    # Create the body of the message (a plain-text and an HTML version).
    text = 'Hi!\n\nThis is a complete list with cases that need action from our Team.\n\n \
        Please open a html version that has been sent with this email for \
        further details'
    html = """\
<html>
<head></head>
<body>

Hola %s!<br> <br>

This is the script being executed and here is the complete list with cases that need action:<br><br>

<p style="text-indent: 5em;">
%s
</p>

Thank you!
</body>
</html>""" % (boss, functions.ListAllConsultantsCases(AllConsultantsCases))
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    functions.sendEmail(msg['From'], msg['To'], msg.as_string(), variables.SMTPServer)
#    print(msg.as_string())


def sendEmailToConsultants(ListOfErrors):
    print("Sending email")
    # Email testing line
    # emailToConsultant(ListOfErrors[0][0], "test", ListOfErrors[0][2])
#    print(functions.ListAllConsultantsCases(ListOfErrors))
    # Sending email to each consultant with his wrong cases
    [emailToConsultant(consultantReport[0], consultantReport[1], consultantReport[2]) for consultantReport in ListOfErrors]
    # Sending emails to Bosses and QM with all our errors.
    for CcPerson in variables.CcEmails:
        emailToBoss(CcPerson[0], CcPerson[1], ListOfErrors)
