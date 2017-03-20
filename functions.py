def RequestorRoleIsPartner(requestorRole):
    return (requestorRole == 'Partner')


def IsLocationPrimary(assetLocPrimary):
    return int(assetLocPrimary)


def partnerInList(Email, Role):
    return ((not ("@hpe.com" in Email)) and (Role == "HPE Internal"))


def assetLocationStatus(status):
    return (status == 'Active')


def locatorIDstart4(locID):
    return (locID[0] == '4')


def sourceIDstart1(accID):
    return (accID[0] == '1')


def countrySubLoc(submitter, location):
    return (submitter == location)


def emailReqContains(email):
    return ("hpe.com" in email[-7:])


def isLocationStatus(location):
    return location == "Active"


def countrySubLocEqual(cSub, aLocation):
    if aLocation == "Russian Federation":
        print(cSub[:6])
        return cSub[:6] == "Russia"
    return cSub == aLocation
