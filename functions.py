def RequestorRoleIsPartner(Email, requestorRole):
    return ((requestorRole == 'Partner') and ("hpe.com" in Email))


def caseRoleIsPartner(requestorRole):
    return (requestorRole == 'Partner')


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
