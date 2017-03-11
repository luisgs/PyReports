import csv
import sys


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
    with open(sys.argv[1],"rt") as ReportCsv:
        next(ReportCsv)     # We skip first line
        reader = csv.reader(ReportCsv)
        data = list(reader)
        row_count = len(data)

    for row in data:
        if len(row) >= 7:
            if List_Cases:  # List is not empty
                consultantCases(row[7], int(row[0]))
            else:
                List_Cases.append([row[7], [int(row[0])]])
        else:   # Row comming now are trash
            break
#        List_Cases.append([row[0], row[7]])
finally:
    ReportCsv.close()

print(List_Cases)
