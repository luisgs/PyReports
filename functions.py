def RequestorRoleIsPartner(requestorRole):
    return (requestorRole == 'Partner')


def IsLocationPrimary(assetLocPrimary):
    return int(assetLocPrimary)


def foo(Email, Role):
    return (Email.find('@hpe.com') and (Role is not 'Non HPE Partner'))


def assetLocationStatus(status):
    return (status == 'Active')


def locatorIDstart4(locID):
    return (locID[0] == '4')


def sourceIDstart1(accID):
    return (accID[0] == '1')


def countrySubLoc(submitter, location):
    return (submitter == location)


def emailReqContains(email):
    return ("hpe.com.am" in email)
