import csv
import sys
import os
import re
import sendEmail
import codecs
import functions
import globalVariables


# ListOfErrors = ['Luis' , 'luis@email.com' , {case1: [ErrorCode]}]
ListOfErrors = []


# Dict of {case: Suggested OppID}
dictCasesOPP = {}


# we bring our dict  of errors
ErrorsDefinition = globalVariables.ErrorsDefinition


# Which types of reports we have?
ListOfReports = ["missOPPID", "PPID miss", "PPID bad"]


def isItAFile(filename):
    "We have a file as arg that exist and it is readable"
    if not (os.path.isfile(filename) and os.access(filename, os.R_OK)):
        sys.stderr.write('ERROR: Filename is not a file OR it is not readable\n')
        sys.exit(1)
    return 1


def printListCases():
    for consultantInfo in ListOfErrors:
        print(consultantInfo[0] + " (" + consultantInfo[1] + "):")
        for case in consultantInfo[2]:
            print("\t"+str(case))
            for Error in consultantInfo[2][case]:
                print("\t\t"+str(ErrorsDefinition[Error]))
                if ((Error == "missOPPID") and (str(case) in dictCasesOPP)):
                    print("\t\t\t Our suggestion is to write: " +
                          str(dictCasesOPP[str(case)]))



def insertConsultCase(Name, Email, CaseNumber, ErrorCode):
    for i in range(len(ListOfErrors)):
        if (ListOfErrors[i][1] == Email):
            if CaseNumber in ListOfErrors[i][2]:
                # if CaseID exist, I append this new error
                # ListOfErrors[i][2][CaseNumber].append(ErrorsDefinition[ErrorCode])
                ListOfErrors[i][2][CaseNumber].append(ErrorCode)
            else:
                # If key (CaseNumber) does not exist, I add it
                # ListOfErrors[i][2][CaseNumber] = [ErrorsDefinition[ErrorCode]]
                ListOfErrors[i][2][CaseNumber] = [ErrorCode]
            return 1
    # List is empty OR new consultant in list!
    ListOfErrors.append([Name, Email,
                         {CaseNumber: [ErrorCode]}])


def whichReportIsIt(CSVfield):
    # We received a string from a csv file that contains CSV report's name
    # we return which tpye of report we are working on
    for i in range(len(ListOfReports)):
        if ListOfReports[i] in CSVfield:
            return ListOfReports[i]
    # eoc -> unknown report!
    return "Unknown"


def missOppId_function(data, CaseID, OwnerEmail, OwnerName, Description,
                       Subject):
    for row in data:
        insertConsultCase(row[OwnerName], row[OwnerEmail],
                          int(row[CaseID]), 'missOPPID')
        # look for a OppID in text
        oppID = returnOPPID(row[Description])

        if not oppID:
            oppID = returnOPPID(row[Subject])
        # In case of Subject or Description have it, insert it!
        if oppID:
            dictCasesOPP.update({row[CaseID]: oppID})
    return 1


def missPPIDbad_function(data, CaseID, OwnerEmail, OwnerName, asLocPrimary,
                         reqEmail, reqRole, asLocStatus, countrySub,
                         asCountryLoc):
    for row in data:
        if not functions.IsLocationPrimary(row[asLocPrimary]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              'LocationNotPrimary')
        if functions.emailReqContains(row[reqEmail]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              'ReqEndHPE')
        if not functions.caseRoleIsPartner(row[reqRole]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              'RoleIsNotPartner')
        if not functions.isLocationStatus(row[asLocStatus]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              'LocStatusDisable')
        if not functions.countrySubLocEqual(row[countrySub],
                                            row[asCountryLoc]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              'countrySubLoc')


def missPIDD_function(data, CaseID, OwnerEmail, OwnerName, ReqEmail, ReqRole,
                      caseBU):
    for row in data:
        if not functions.RequestorRoleIsPartner(row[ReqEmail], row[ReqRole]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              'RoleIsNotPartner')
        if functions.BUisMissing(row[caseBU]):
            insertConsultCase(row[OwnerName], row[OwnerEmail],
                              int(row[CaseID]), 'BUisMissing')
        if functions.emailReqContains(row[ReqEmail]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              "ReqEndHPE")
        # All these cases do NOT have Asset Location ID
        insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                          'PPIDmiss')


def returnOPPID(text):
    oppID = 0
    match = re.search(r"\d{10}", text)
    # If-statement after search() tests if it succeeded
    if match:
        oppID = match.group(0)
    return oppID


reportsIndexesDict = {}


# def retreivingFileIndexes(fileheader):
# WE receive a CSV header and we take header indexes for our reports
# We read CSV header!
# Specific Index values for reports
# Common Index Values for all type of reports
#    ownerEmailIndex = fileheader.index('Case Owner eMail')
#    caseIndex = fileheader.index('Case Number')    # caseID
#    ownerName = fileheader.index('Case Owner')
#    if ("PPID bad" in reportName):
#        asLocPrimary = fileheader.index('Asset Location: Primary')
#        asLocStatus = fileheader.index('Asset Location: Location Status')
#        countrySub = fileheader.index('Country of Submitter')
#        reqRoleIndex = fileheader.index('Requestor Role')  # Req Role
#        asCountryLoc = fileheader.index('Asset Location: Country')
#        reqEmailIndex = fileheader.index('Case Requestor Email')
#    elif ("PPID miss" in reportName):
#        reqRoleIndex = fileheader.index('Requestor Role')  # Req Role
#        caseBU = fileheader.index('BU')
#        reqEmailIndex = fileheader.index('Case Requestor Email')
#    elif ("missOPPID" in reportName):
#        emailSubject = fileheader.index('Subject')
#        emailDescription = fileheader.index('Case description')
#    else:
#        sys.stderr.write("ERROR: REport is unknown so we can take headers")
#    return 1


def generateReport(fname):
    isItAFile(fname)
    try:
        with codecs.open(fname, 'r', 'iso-8859-1') as ReportCsv:
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
        # Python closes files automatically but... what the hell!
        ReportCsv.close()

    # We send to each function all csv line (except header and tail [1:-7] +
    # We send them ->index value<- of each data field.
    if ("missOPPID" in reportName):
        missOppId_function(data[1:-7], caseIndex, ownerEmailIndex, ownerName,
                           emailDescription, emailSubject)
    elif ("PPID bad" in reportName):
        missPPIDbad_function(data[1:-7], caseIndex, ownerEmailIndex, ownerName,
                             asLocPrimary, reqEmailIndex, reqRoleIndex,
                             asLocStatus, countrySub, asCountryLoc)
    elif ("PPID miss" in reportName):
        missPIDD_function(data[1:-7], caseIndex, ownerEmailIndex, ownerName,
                          reqEmailIndex, reqRoleIndex, caseBU)
    # print cases per Consultant!!
#    printListCases()
    # emailToConsultant()
    sendEmail.sendEmailToConsultants(ListOfErrors)

def main():
    for i in range(1, len(sys.argv)):
        generateReport(sys.argv[i])
    printListCases()


if __name__ == "__main__":
    sys.exit(main())
