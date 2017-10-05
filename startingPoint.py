import os
import glob
import time
import py_reports

# Reports will be downloaded in automatically in our Download folder.
# Downloads
os.system('start chrome "https://hp.my.salesforce.com/00O27000007XetZ?isdtp=mn&export=1&enc=iso-8859-1&xf=csv"')
os.system('start chrome "https://hp.my.salesforce.com/00O27000007Xezh?isdtp=mn&export=1&enc=iso-8859-1&xf=csv"')
os.system('start chrome "https://hp.my.salesforce.com/00O27000007UA3S?isdtp=mn&export=1&enc=iso-8859-1&xf=csv"')
# we need to wait so we can download our reports and later look for them
print("\\\\Downloading your report files... it might take time.")
for i in range(10,-1,-1):
	print("Waiting... %s seconds" % (i))
	time.sleep(1)
print("\\\\ Ready for execution!")

# With our reports in our Download folder, we can look for the three newest report*csv files
# Default path is Downloads
path = os.path.join(os.path.expanduser("~"), "Downloads\\report*.csv")
files = glob.glob(path)

# first CSV
firstCSV=max(files , key = os.path.getctime)
files.remove(max(files , key = os.path.getctime))

# Second CSV
secondCSV=max(files , key = os.path.getctime)
files.remove(max(files , key = os.path.getctime))

# Third CSV
thirdCSV=max(files , key = os.path.getctime)


# We call our py_reports.
py_reports.main([firstCSV, secondCSV, thirdCSV])

# Delete those CSV files, we do not need them anymore.
print("Removing report files!")
os.remove(firstCSV)
os.remove(secondCSV)
os.remove(thirdCSV)
