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


# Our final list of errors that we will send to sendEmail function.
# ==> ['Luis', 'luis@email.com', {Case1: [ErrorDEFINITION-SOLUTION]}]
ReadyToSend= []


# we bring our dict  of errors
ErrorsDefinition = globalVariables.ErrorsDefinition


# Which types of reports we have?
ListOfReports = ["missOPPID", "PPID miss", "PPID bad"]


def isItAFile(filename):
    "We have a file as arg that exist and it is readable"
    if not (os.path.isfile(filename) and os.access(filename, os.R_OK)):
        sys.stderr.write('ERROR: Path is not a file OR not readable\n')
        sys.exit(1)
    return 1


def printListCases():
    for consultantInfo in ListOfErrors:		# take the first consultant 
        print(consultantInfo[0] + " (" + consultantInfo[1] + "):") # print his name and email
        for case in consultantInfo[2]:		# take his dict of cases:errors
            print("\t"+str(case))		# print Case Number
            for Error in consultantInfo[2][case]:
                print("\t\t"+str(Error))	# print his Error!


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
        # look for a OppID in text
        oppID = returnOPPID(row[Description])
        if not oppID:
            oppID = returnOPPID(row[Subject])
        # In case of Subject or Description have it, insert it!
        if oppID:
            dictCasesOPP.update({row[CaseID]: oppID})
            insertConsultCase(row[OwnerName], row[OwnerEmail],
                          int(row[CaseID]), ErrorsDefinition['missOPPID'] + "\t We beleive is this: " + oppID)
        else: # We could not get the OppID from the email!
            insertConsultCase(row[OwnerName], row[OwnerEmail],
                          int(row[CaseID]), ErrorsDefinition['missOPPID'])
    return 1


def missPPIDbad_function(data, CaseID, OwnerEmail, OwnerName, asLocPrimary,
                         reqEmail, reqRole, asLocStatus, countrySub,
                         asCountryLoc):
    for row in data:
        if not functions.IsLocationPrimary(row[asLocPrimary]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              ErrorsDefinition['LocationNotPrimary'])
        if functions.emailReqContains(row[reqEmail]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              ErrorsDefinition['ReqEndHPE'])
        if not functions.caseRoleIsPartner(row[reqRole]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              ErrorsDefinition['RoleIsNotPartner'])
        if not functions.isLocationStatus(row[asLocStatus]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              ErrorsDefinition['LocStatusDisable'])
        if not functions.countrySubLocEqual(row[countrySub],
                                            row[asCountryLoc]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              ErrorsDefinition['countrySubLoc'])


def missPIDD_function(data, CaseID, OwnerEmail, OwnerName, ReqEmail, ReqRole,
                      caseBU):
    for row in data:
        if not functions.RequestorRoleIsPartner(row[ReqEmail], row[ReqRole]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              ErrorsDefinition['RoleIsNotPartner'])
        if functions.BUisMissing(row[caseBU]):
            insertConsultCase(row[OwnerName], row[OwnerEmail],
                              int(row[CaseID]), ErrorsDefinition['BUisMissing'])
        if functions.emailReqContains(row[ReqEmail]):
            insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                              ErrorsDefinition['ReqEndHPE'])
        # All these cases do NOT have Asset Location ID
        insertConsultCase(row[OwnerName], row[OwnerEmail], int(row[CaseID]),
                          ErrorsDefinition['PPIDmiss'])


def returnOPPID(text):
    oppID = 0
    match = re.search(r"\d{10}", text)
    # If-statement after search() tests if it succeeded
    if match:
        oppID = match.group(0)
    return oppID


reportsIndexesDict = {}


def generateReport(fname):
    isItAFile(fname)
    try:
        with codecs.open(fname, 'r', 'iso-8859-1') as ReportCsv:
            reader = csv.reader(ReportCsv)
            data = list(reader)
            # with which report are we working on?
            # report definition is set at the bottom of the file
            reportName = whichReportIsIt(data[-5][0])
            # print(reportName)
            if ("Unknown" in reportName):
                sys.stderr.write("ERROR: %s has not been recognize\n" % fname)
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


def main(argv):
    for i in range(len(argv)):
        generateReport(argv[i])
    sendEmail.sendEmailToConsultants(ListOfErrors)
    # Print in the regular output, CLI, all the cases
    # print(functions.ListAllConsultantsCases(ListOfErrors))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
