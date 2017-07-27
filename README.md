# PyReports
PyReports sends an email to each consultant with misfillings fields at SFDC. It gets data from internal csv reports. 

## Summary
We close cases in SFDC and some of them are not completed correct fulfilled. This script helps us so it sends emails to each consultant that appears in the reports. It sends a list of his cases that need actions as well as which corrections are needed. 
Admin retrieves these reports and execute our pyreport script point to them. It will send an individual email to each consultant with a set of points to correct.

## Requirements
- Report files
  These reports are generated via SalesForce according to a well known report we have. Meaning, we know which columns they have.
- Email account with rights so we can send email through it using it as a gateway
- Python 

## How to execute it?
./python py_reports.py reports.csv [report2.csv]


