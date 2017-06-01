# PyReports
We need some scripts to speed up reporting at work.


## Summary
We close cases in SFDC that are not completed correclty filled in. Our tool helps us to send emails to each consultant with a list of their cases that need actions as well as which correction are needed. 
Admin retrieves those reports and execute our py script which will send an individual email to each consultant with a set of points to correct.

## Requirements
- XLS files
  These reports are generated via SalesForce according to a well known report we have. Meaning, we know which columns they have.
- email account with rights so we can send email through it. 


