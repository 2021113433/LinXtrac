#####################################################################
# Imports
#####################################################################

import os
from customtkinter import filedialog
from tkinter import messagebox
from datetime import datetime

#####################################################################
# Get Directory
#####################################################################

def getDirectory():

    global currentWorkingDirectory
    global rootDirectory
    global mainFolder
    global dateName

    currentWorkingDirectory_temp = os.getcwd()
    rootDirectory_temp = filedialog.askdirectory()

    dateName_temp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    folderName = "LinXtrac - Linux Extractions Systems Result"

    combinedName = os.path.join(currentWorkingDirectory_temp,dateName_temp)
    os.mkdir(combinedName)
    mainFolder_temp = os.path.join(combinedName,folderName)
    os.mkdir(mainFolder_temp)

    dateName = dateName_temp
    currentWorkingDirectory = currentWorkingDirectory_temp
    rootDirectory = rootDirectory_temp
    mainFolder = mainFolder_temp

    if (rootDirectory_temp == ""):
        messagebox.showinfo("Exit", "No directory chosen. Exiting...")
        exit()

    return

#####################################################################
# Report
#####################################################################

def generateReport(OSInfo):

    reportPath = os.path.join(mainFolder, "LinXtrac Report.html")
    with open(reportPath, "w") as reportFile:
        # Write HTML markup
        reportFile.write("<html>\n")
        reportFile.write("<head>\n")
        reportFile.write("<title>HTML Report</title>\n")
        reportFile.write("</head>\n")
        reportFile.write("<body>\n")
        
        # Write own data
        reportFile.write("<h1>Report Data</h1>\n")
        reportFile.write("<p>{}</p>\n".format(OSInfo))
        
        # Close HTML markup
        reportFile.write("</body>\n")
        reportFile.write("</html>\n")

def appendReport(data):

    reportPath = os.path.join(mainFolder, "report.html")
    with open(reportPath, "a") as reportFile:
        # Append data to existing HTML report
        reportFile.write("<h1>Appended Data</h1>\n")
        reportFile.write("<p>{}</p>\n".format(data))

def closeReport():

    reportPath = os.path.join(mainFolder, "report.html")
    with open(reportPath, "a") as reportFile:
        reportFile.write("</body>\n")
        reportFile.write("</html>\n")

    return
