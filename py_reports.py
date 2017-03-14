import csv
import sys
import os
import sendEmail

# List_Cases = [ [ 'Luis' , 'email@email.com' , [ '123456' , '789456' ] ] ]
List_Cases = []


def consultantCases(Consultant, ConsultantEmail, CaseNumber):
    "We will insert in Global_Cases[], consultant cases"
    " case [0] = Consultant"
    " case [1] = CaseNumber"
    for i in range(len(List_Cases)):
        if Consultant == List_Cases[i][0]:
            List_Cases[i][2].append(CaseNumber)
            return
    List_Cases.append([Consultant, ConsultantEmail, [CaseNumber]])


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
    for consultantInfo in List_Cases:
        print(consultantInfo[0] + " (" + consultantInfo[1] + "):")
        for cases in consultantInfo[2]:
            print("\t %i" % cases)


def emailToConsultant():
    for consultantReport in List_Cases:
        sendEmail.emailToConsultant(consultantReport[0], consultantReport[1])


def main():
    doWeHaveAFile()
    try:
        with open(sys.argv[1], 'rt') as ReportCsv:
            reader = csv.reader(ReportCsv)
            data = list(reader)
            caseIndex = data[0].index('Case Number')    # caseID
            ownerIndex = data[0].index('Case Owner')    # caseOwner
            ownerEmailIndex = data[0].index('Case Owner eMail')  # ownerEmail
    except (IOError):
        sys.stderr.write("ERROR: File (%s) cannot be openned\n" % sys.argv[1])
        sys.exit(1)
    except ValueError:
        sys.stderr.write("ERROR: Error CSV header value is missing\n")
        sys.exit(1)
    else:
        for row in data[1:-7]:  # Skip CSV header and last lines!
            if List_Cases:  # Global list HAS data
                consultantCases(row[ownerIndex], row[ownerEmailIndex],
                                int(row[caseIndex]))
            else:   # if list is empty
                List_Cases.append([row[ownerIndex], row[ownerEmailIndex],
                                   [int(row[caseIndex])]])
    finally:
        # Python closes files automatically but... what the hell
        ReportCsv.close()

    # print cases per Consultant!!
    printListCases()
    # print(List_Cases)
    emailToConsultant()


if __name__ == "__main__":
    main()
