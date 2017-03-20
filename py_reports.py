import csv
import sys
import os
import sendEmail
import codecs
import functions

# ListOfErrors = ['Luis' , 'email@email.com' , {case1: ['Error1']}]
ListOfErrors = []


def doWeHaveAFile():
    "We have a file as arg that exist and it is readable"
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: sys.argv[0], Please pass me a file!\n')
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write('ERROR: File does NOT exist\n')
        sys.exit(1)
    return 1


def printListCases():
    for consultantInfo in ListOfErrors:
        print(consultantInfo[0] + " (" + consultantInfo[1] + "):")
        for case in consultantInfo[2]:
            print("\t"+str(case))
            for Error in consultantInfo[2][case]:
                print("\t\t"+str(Error))


def emailToConsultant():
    for consultantReport in ListOfErrors:
        sendEmail.emailToConsultant(consultantReport[0],
                                    consultantReport[1], consultantReport[2])
        break


def insertConsultCase(Name, Email, CaseNumber, ErrorCode):
    for i in range(1, len(ListOfErrors)):
        if (ListOfErrors[i][1] == Email):
            if CaseNumber in ListOfErrors[i][2]:
                # if CaseID exist, I append this new error
                ListOfErrors[i][2][CaseNumber].append(ErrorCode)
            else:
                # If key (CaseNumber) does not exist, I add it
                ListOfErrors[i][2][CaseNumber] = [ErrorCode]
            return
    # List is empty OR new consultant in list!
    ListOfErrors.append([Name, Email, {CaseNumber: [ErrorCode]}])


def main():
    doWeHaveAFile()
    try:
        with codecs.open(sys.argv[1], 'r', 'iso-8859-1') as ReportCsv:
            reader = csv.reader(ReportCsv)
            data = list(reader)
            # We read CSV header!
            # Specific Index values for reports
            if 'Asset Location: Primary' in data[0]:
                reportNumber = 1
                asLocPrimary = data[0].index('Asset Location: Primary')
                asLocStatus = data[0].index('Asset Location: Location Status')
                countrySub = data[0].index('Country of Submitter')
                asCountryLoc = data[0].index('Asset Location: Country')
            else:
                reportNumber = 2
            # Common Index Values for all types reports
            ownerEmailIndex = data[0].index('Case Owner eMail')
            caseIndex = data[0].index('Case Number')    # caseID
            ownerIndex = data[0].index('Case Owner')
            reqEmailIndex = data[0].index('Case Requestor Email')
            reqRoleIndex = data[0].index('Requestor Role')  # Req Role
    except (IOError):
        sys.stderr.write("ERROR: File (%s) cannot be openned\n" % sys.argv[1])
        sys.exit(1)
    except ValueError:
        sys.stderr.write("ERROR: Error CSV header value is missing\n")
        sys.exit(1)
    else:
        if reportNumber == 1:
            for row in data[1:-7]:  # Skip CSV header and last lines!
                if not functions.IsLocationPrimary(row[asLocPrimary]):
                    insertConsultCase(row[ownerIndex], row[ownerEmailIndex],
                                      int(row[caseIndex]), 'LocationNotPrimary')
                if functions.emailReqContains(row[reqEmailIndex]):
                    insertConsultCase(row[ownerIndex], row[ownerEmailIndex],
                                      int(row[caseIndex]), 'Requestor email ends hpe.com')
                if not functions.caseRoleIsPartner(row[reqRoleIndex]):
                    insertConsultCase(row[ownerIndex], row[ownerEmailIndex],
                                      int(row[caseIndex]), 'Role Is not Partner. Change it!')
                if not functions.isLocationStatus(row[asLocStatus]):
                    insertConsultCase(row[ownerIndex], row[ownerEmailIndex],
                                      int(row[caseIndex]), 'LocationStatusIs DISABLE')
                if not functions.countrySubLocEqual(row[countrySub], row[asCountryLoc]):
                    insertConsultCase(row[ownerIndex], row[ownerEmailIndex],
                                      int(row[caseIndex]), 'Countries does NOT match')
        elif reportNumber == 2:
            for row in data[1:-7]:  # Skip CSV header and last lines!
                if functions.RequestorRoleIsPartner(row[reqEmailIndex], row[reqRoleIndex]):
                    # print("Role is Partner %s" % row[caseIndex])
                    insertConsultCase(row[ownerIndex], row[ownerEmailIndex],
                                      int(row[caseIndex]), 'Role Is Partner. Change it!')
                if functions.partnerInList(row[reqEmailIndex], row[reqRoleIndex]):
                    # print("foo %s" % row[caseIndex])
                    insertConsultCase(row[ownerIndex], row[ownerEmailIndex],
                                      int(row[caseIndex]), 'Requestor is NOT HPE!')
    finally:
        # Python closes files automatically but... what the hell
        ReportCsv.close()
    # print cases per Consultant!!
    printListCases()
#    emailToConsultant()


if __name__ == "__main__":
    main()
