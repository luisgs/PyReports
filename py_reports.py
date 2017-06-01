import csv
import sys
import os
import sendEmail
import codecs
import functions

# ListOfErrors = ['Luis' , 'luis@email.com' , {case1: ['Error1']}]
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
    [sendEmail.emailToConsultant(consultantReport[0],
                                 consultantReport[1],
                                 consultantReport[2]) for
     consultantReport in ListOfErrors]


ErrorsDefinition = {"LocationNotPrimary": "Case Location is NOT primary",
                    "ReqEndHPE": "Requestor Email ends with @hpe.com",
                    "RoleIsNotPartner": "Requestor Role needs to be " +
                    "change to Partner",
                    "LocStatusDisable": "Assest Location Status " +
                    "is set to Disable",
                    "countrySubLoc": "Country Submitter and " +
                    "Asset Country Location does NOT match",
                    "BUisMissing": "BU is empty, complete it!",
                    "PPIDmiss": "This case has not Asset Location",
                    "ReqIsNotHPE": "Requestor Role needs to be HPE",
                    "missOPPID": "Opportunity ID provided but not " +
                    "fulfilled in the case."}


def insertConsultCase(Name, Email, CaseNumber, ErrorCode):
    for i in range(len(ListOfErrors)):
        if (ListOfErrors[i][1] == Email):
            if CaseNumber in ListOfErrors[i][2]:
                # if CaseID exist, I append this new error
                ListOfErrors[i][2][CaseNumber].append(ErrorsDefinition[ErrorCode])
            else:
                # If key (CaseNumber) does not exist, I add it
                ListOfErrors[i][2][CaseNumber] = [ErrorsDefinition[ErrorCode]]
            return
    # List is empty OR new consultant in list!
    ListOfErrors.append([Name, Email,
                         {CaseNumber: [ErrorsDefinition[ErrorCode]]}])


ListOfReports = ["missOPPID", "PPID miss", "PPID bad"]


def whichReportIsIt(CSVfield):
    # We received a string from a csv file that contains CSV report's name
    # we return which tpye of report we are working on
    for i in range(len(ListOfReports)):
        if ListOfReports[i] in CSVfield:
            return ListOfReports[i]
    # eoc -> unknown report!
    return "Unknown"


def missOppId_function(data, Subject, Description, OwnerEmail,
                       CaseID, OwnerName):
    for row in data:
        insertConsultCase(row[OwnerName], row[OwnerEmail],
                          int(row[CaseID]), 'missOPPID')
    return 1


def main():
    doWeHaveAFile()
    try:
        with codecs.open(sys.argv[1], 'r', 'iso-8859-1') as ReportCsv:
            reader = csv.reader(ReportCsv)
            data = list(reader)
            # with which report are we working on?
            # report definition is set at the bottom of the file
            reportName = whichReportIsIt(data[-5][0])
            print(reportName)
            if ("Unknown" in reportName):
                sys.stderr.write("ERROR: This report file has not been recognize\n")
                sys.exit(1)
            # We read CSV header!
            # Specific Index values for reports
            # Common Index Values for all type of reports
            ownerEmailIndex = data[0].index('Case Owner eMail')
            caseIndex = data[0].index('Case Number')    # caseID
            ownerName = data[0].index('Case Owner')
            if ("PPID bad" in reportName):
                asLocPrimary = data[0].index('Asset Location: Primary')
                asLocStatus = data[0].index('Asset Location: Location Status')
                countrySub = data[0].index('Country of Submitter')
                reqRoleIndex = data[0].index('Requestor Role')  # Req Role
                asCountryLoc = data[0].index('Asset Location: Country')
                reqEmailIndex = data[0].index('Case Requestor Email')
            elif ("PPID miss" in reportName):
                reqRoleIndex = data[0].index('Requestor Role')  # Req Role
                caseBU = data[0].index('BU')
                reqEmailIndex = data[0].index('Case Requestor Email')
            elif ("missOPPID" in reportName):
                emailSubject = data[0].index('Subject')
                emailDescription = data[0].index('Case description')
    except (IOError):
        sys.stderr.write("ERROR: File (%s) cannot be openned\n" % sys.argv[1])
        sys.exit(1)
    except ValueError:
        sys.stderr.write("ERROR: Error CSV header value is missing\n")
        sys.exit(1)
    finally:
        # Python closes files automatically but... what the hell
        ReportCsv.close()

    if ("missOPPID" in reportName):
        missOppId_function(data[1:-7], emailSubject, emailDescription,
                            ownerEmailIndex, caseIndex, ownerName)
    elif ("PPID bad" in reportName):
        for row in data[1:-7]:  # Skip CSV header and last lines!
            if not functions.IsLocationPrimary(row[asLocPrimary]):
                insertConsultCase(row[ownerName], row[ownerEmailIndex],
                                    int(row[caseIndex]), 'LocationNotPrimary')
            if functions.emailReqContains(row[reqEmailIndex]):
                insertConsultCase(row[ownerName], row[ownerEmailIndex],
                                    int(row[caseIndex]), 'ReqEndHPE')
            if not functions.caseRoleIsPartner(row[reqRoleIndex]):
                insertConsultCase(row[ownerName], row[ownerEmailIndex],
                                    int(row[caseIndex]), 'RoleIsNotPartner')
            if not functions.isLocationStatus(row[asLocStatus]):
                insertConsultCase(row[ownerName], row[ownerEmailIndex],
                                    int(row[caseIndex]), 'LocStatusDisable')
            if not functions.countrySubLocEqual(row[countrySub],
                                                row[asCountryLoc]):
                insertConsultCase(row[ownerName], row[ownerEmailIndex],
                                    int(row[caseIndex]), 'countrySubLoc')
    elif ("PPID miss" in reportName):
        for row in data[1:-7]:  # Skip CSV header and last lines!
            if not functions.RequestorRoleIsPartner(row[reqEmailIndex],
                                                row[reqRoleIndex]):
                insertConsultCase(row[ownerName], row[ownerEmailIndex],
                                    int(row[caseIndex]), 'RoleIsNotPartner')
            if functions.BUisMissing(row[caseBU]):
                insertConsultCase(row[ownerName], row[ownerEmailIndex],
                                    int(row[caseIndex]), 'BUisMissing')
#            if functions.partnerInList(row[reqEmailIndex],
#                                        row[reqRoleIndex]):
                # print("foo %s" % row[caseIndex])
#                insertConsultCase(row[ownerName], row[ownerEmailIndex],
#                                    int(row[caseIndex]), 'ReqIsNotHPE')
            # All these cases do NOT have Asset Location ID
            insertConsultCase(row[ownerName], row[ownerEmailIndex],
                                int(row[caseIndex]), 'PPIDmiss')
    # print cases per Consultant!!
    printListCases()
    # emailToConsultant()


if __name__ == "__main__":
    main()
