def RequestorRoleIsPartner(Email, requestorRole):
    if ("Partner" in requestorRole):
        return True
    return False


def caseRoleIsPartner(requestorRole):
    return (requestorRole == 'Partner')


def BUisMissing(BU):
    print(BU)
    return (BU)


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
