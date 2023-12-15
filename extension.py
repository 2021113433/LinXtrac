#####################################################################
# Imports and setups
#####################################################################

import os
import tempfile
from customtkinter import filedialog
from tkinter import messagebox
from datetime import datetime

messages = []  

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
    folderName = "LinXtrac - Linux Extraction System Result"

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

def generateReport(osi, host, time):

    reportPath = os.path.join(mainFolder, "LinXtrac Report.html")
    with open(reportPath, "w") as reportFile:

        reportFile.write("<html>\n")
        reportFile.write("<head>\n")
        reportFile.write("<title>LinXtrac - Linux Extraction System Report</title>\n")
        reportFile.write("<h1>LinXtrac</h1>\n")
        reportFile.write("<h2>Linux Extractions System Report</h2>\n")
        reportFile.write("</head>\n")
        reportFile.write("<body>\n")
        
        reportFile.write("<h3>OS Information</h3>\n")
        reportFile.write("<p>OS: {}<br>Host: {}<br>Time: {}</p>\n".format(osi, host, time))

def appendReport(data):

    reportPath = os.path.join(mainFolder, "LinXtrac Report.html")
    with open(reportPath, "a") as reportFile:
        
        reportFile.write("<h1>Appended Data</h1>\n")
        reportFile.write("<p>{}</p>\n".format(data))

def closeReport():

    reportPath = os.path.join(mainFolder, "LinXtrac Report.html")
    with open(reportPath, "a") as reportFile:
        reportFile.write("</body>\n")
        reportFile.write("</html>\n")

    return

#####################################################################
# OS Information
#####################################################################

def getInfo():

    usrDirectory = "usr"
    libDirectory = "lib"
    etcDirectory = "etc"
    osToSearch = "os-release"
    hostToSearch = "hostname"
    timeToSearch = "localtime"

    ### os-release

    for relPath,dirs,files in os.walk(rootDirectory):
        if(usrDirectory in dirs):
            firstLayer = os.path.join(rootDirectory,relPath,usrDirectory)
            break

    for relPath,dirs,files in os.walk(firstLayer):
        if(libDirectory in dirs):
            targetedLayer = os.path.join(firstLayer,relPath,libDirectory)
            break
    
    for relPath,dirs,files in os.walk(targetedLayer):
        if(osToSearch in files):
            osPath = os.path.join(targetedLayer,relPath,osToSearch)
            break
        else:
            osPath = False
    
    osp = tempfile.NamedTemporaryFile(delete=False)
    if osPath:
        with open(osPath, "r") as input:
            for line in input:
                osp.write(line.encode())
    osp.close()
    
    ### hostname

    for relPath,dirs,files in os.walk(rootDirectory):
        if(etcDirectory in dirs):
            targetDirectory = os.path.join(rootDirectory,relPath,etcDirectory)
            break
    
    for relPath,dirs,files in os.walk(targetDirectory):
        if(hostToSearch in files):
            hostPath = os.path.join(targetDirectory,relPath,hostToSearch)
            break
        else:
            hostPath = False

    hst = tempfile.NamedTemporaryFile(delete=False)
    if hostPath:
        with open(hostPath, "r") as input:
            for line in input:
                hst.write(line.encode())
    hst.close()

    ### zoneinfo

    for relPath,dirs,files in os.walk(rootDirectory):
        if(etcDirectory in dirs):
            timeDirectory = os.path.join(rootDirectory,relPath,etcDirectory)
            break
    
    for relPath,dirs,files in os.walk(timeDirectory):
        if(timeToSearch in files):
            timePath = os.path.join(timeDirectory,relPath,timeToSearch)
            break
        else:
            timePath = False

    znf = tempfile.NamedTemporaryFile(delete=False)
    if timePath:
        with open(timePath, "r") as input:
            for line in input:
                znf.write(line.encode())
    znf.close()

    ###

    with open(osp.name, 'r') as file:
        os_data = file.read()
    with open(hst.name, 'r') as file:
        host_data = file.read()
    with open(znf.name, 'r') as file:
        time_data = file.read()

    generateReport(os_data, host_data, time_data)
    os.remove(osp.name)
    os.remove(hst.name)
    os.remove(znf.name)

    return