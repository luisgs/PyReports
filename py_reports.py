import csv
import sys
# import warnings

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

try:
    with open(sys.argv[1], 'rt') as ReportCsv:
        next(ReportCsv)     # We skip first line, it is trash
        reader = csv.reader(ReportCsv)
        data = list(reader)
        row_count = len(data)
except IOError:
    print("Err: input file has not been declare or problem while openning")
    raise
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

print(List_Cases)
