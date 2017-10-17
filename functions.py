import smtplib

def RequestorRoleIsPartner(Email, requestorRole):
    if ("Partner" in requestorRole):
        return True
    return False


def caseRoleIsPartner(requestorRole):
    return (requestorRole == 'Partner')


def BUisMissing(BU):
    # if BU empty, then return not Flase = True = missing!
    return not BU


def IsLocationPrimary(assetLocPrimary):
    return int(assetLocPrimary)


def partnerInList(Email, Role):
    return ((not ("@hpe.com" in Email)) and (Role != "Non HPE Partner"))


def assetLocationStatus(status):
    return (status == 'Active')


def locatorIDstart4(locID):
    return (locID[0] == '4')


def sourceIDstart1(accID):
    return (accID[0] == '1')


def emailReqContains(email):
    return ("hpe.com" in email[-7:])


def isLocationStatus(location):
    return location == "Active"


def countrySubLocEqual(cSub, aLocation):
    if aLocation == "Russian Federation":
        return cSub[:6] == "Russia"
    return cSub == aLocation


def ListAllConsultantsCases(ListOfErrors):
    output="<ul>"
    href='https://hp.my.salesforce.com/_ui/search/ui/UnifiedSearchResults?searchType=2&sen=500&sen=00O&str='
    for consultantInfo in ListOfErrors:         # take the first consultant
        output+=("<li>" + consultantInfo[0] + " (" + consultantInfo[1] + "):</li> <ol>") # print his name and email
        for case in consultantInfo[2]:          # take his dict of cases:errors
            output+=('<li><a href=\"%s%s\">%s</a>:</li><ul>') % (href,str(case),str(case))               # print Case Number
            for Error in consultantInfo[2][case]:
                output+=("<li>"+str(Error)+"</li>")        # print his Error!
            output+="</ul>"
        output+="</ol>"
    return output+"</ul>"


def sendEmail(From, to, msg, SMTP):
    # Send the message via local SMTP server.
    try:
        s = smtplib.SMTP(SMTP)
	#s.starttls()                   # SMTP of HPE does not allow TLS
        s.ehlo()
        # s.login(variables.emailFrom)  # if we are in the Copr net. No need of PASSW
        # s.login(variables.emailFrom, variables.password)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(From, to, msg)
        s.quit()
    except:
        print("Error sending emails!")
