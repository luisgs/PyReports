def RequestorRoleIsPartner(requestorRole):
    return (requestorRole == 'Partner')


def foo(Email, Role):
    return (Email.find('@hpe.com') and (Role is not 'Non HPE Partner'))
