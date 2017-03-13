import csv
import sys
import os
import sendEmail

# List_Cases = [ [ 'Luis' , [ '123456' , '789456' ] ] , [ 'Javi' , [ '123' ] ] ]
List_Cases = []


def consultantCases(Consultant, CaseNumber):
    "We will insert in Global_Cases[], consultant cases"
    " case [0] = Consultant"
    " case [1] = CaseNumber"
    for i in range(len(List_Cases)):
        if Consultant == List_Cases[i][0]:
            List_Cases[i][1].append(CaseNumber)
            return
    List_Cases.append([Consultant, [CaseNumber]])


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
        print(consultantInfo[0]+":")
        for cases in consultantInfo[1]:
            print("\t %i" % cases)


def emailToConsultant():
    for consultantReport in List_Cases:
        sendEmail.emailToConsultant(consultantReport[0], consultantReport[1])


def main():
    doWeHaveAFile()
    try:
        with open(sys.argv[1], 'rt') as ReportCsv:
            next(ReportCsv)     # We skip first line, it is trash
            reader = csv.reader(ReportCsv)
            data = list(reader)
            # row_count = len(data)
    except (IOError):
        sys.stderr.write("ERROR: File (%s) cannot be openned" % sys.argv[1])
        sys.exit(1)
    else:
        for row in data:
            if len(row):        # if we have data!
                if List_Cases:  # Global list HAS data
                    consultantCases(row[7], int(row[0]))
                else:
                    List_Cases.append([row[7], [int(row[0])]])
            else:   # Rows comming after are trash
                break
    finally:
        # Python closes files automatically but... what the hell
        ReportCsv.close()

    # print cases per Consultant!!
    printListCases()
    # print(List_Cases)
    emailToConsultant()


if __name__ == "__main__":
    main()
