# PyReports
PyReports is a script that will download our perdonal SFDC reports, manage them and send an email to each of the consultants which their action is required.

## Summary
On of our daily tasks, besides of ansewring emails, is to fulfill all the required fields on the case. Sometimes, we forget or these fields are wrongly written. This script helps us in the way that each consultant, with errors in his cases, will receive an email with a list of cases that need his attention as well as the list of errors and actions that need to be taken. 

Script retrieves these reports from a well known url. Reports are formatted in the way we want so script only estructure them and send an email.

## Requirements
- Pyton (2 or 3) needs to be installed.
- Script needs to be executed within our HPE intranet. 
	- Needs to be logged in SFDC (+access to our reports)
	- HPE SMTP server is accesible only via our intranet.
- (Windows) Script needs to run under admin rights.



## How to execute it?
- Windows: Execute a .bat script:
	PyReports.bat
- Linux:
	./python startingPoint.py


