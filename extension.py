#####################################################################
# Imports and setups
#####################################################################

import os
import tempfile
import customtkinter
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
# File Crawler 
#####################################################################

def fileCrawler(root_directory, directories_to_search, file_to_search):
    for directory in directories_to_search:
        filePath = os.path.join(root_directory, directory, file_to_search)
        if os.path.exists(filePath):
            yield filePath
    return

def fileCrawlerAdvanced(root_directory, directories_to_search, file_to_search):
    for directory in directories_to_search:
        for relPath, dirs, files in os.walk(root_directory):
            if directory in dirs:
                root_directory = os.path.join(root_directory, relPath, directory)
                break
        for relPath, dirs, files in os.walk(root_directory):
            if file_to_search in files:
                return os.path.join(root_directory, relPath, file_to_search)
    return False

#####################################################################
# Report
#####################################################################

def generateReport(osi, host, timez):

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
        reportFile.write("<p>OS: {}<br>Host: {}<br>Time: {}</p>\n".format(osi, host, timez))

        return

def appendReport(data):

    reportPath = os.path.join(mainFolder, "LinXtrac Report.html")
    with open(reportPath, "a") as reportFile:
        reportFile.write("<p>{}</p>\n".format(data))
    return

def closeReport():

    reportPath = os.path.join(mainFolder, "LinXtrac Report.html")
    with open(reportPath, "a") as reportFile:
        reportFile.write("</body>\n")
        reportFile.write("</html>\n")

    return

#####################################################################
# Check Extraction Status
#####################################################################

def checkExtractionStatus(stat, extracted_data_dir):
    if os.path.exists(extracted_data_dir):
        stat.configure(text="Extracted")
    else:
        stat.configure(text="Not Extracted")

#####################################################################
# OS Information
#####################################################################

def getInfo():

    usrDirectories = ["usr", "lib"]
    etcDirectories = ["etc"]
    filesToSearch = [("os-release", usrDirectories), ("hostname", etcDirectories), ("localtime", etcDirectories)]

    data = []
    for fileToSearch, directories in filesToSearch:
        for directory in directories:
            filePath = fileCrawlerAdvanced(rootDirectory, [directory], fileToSearch)
            tempFile = tempfile.NamedTemporaryFile(delete=False)
            if filePath:
                with open(filePath, "r") as input:
                    for line in input:
                        tempFile.write(line.encode())
            else:
                tempFile.write("File not found".encode())
            tempFile.close()
            with open(tempFile.name, 'r') as file:
                data.append(file.read())
            os.remove(tempFile.name)
            break  

    generateReport(*data)

    return

#####################################################################
# User Account Data
#####################################################################

def getUserAccountInfo(stat, menuFrame):

    progressbar = customtkinter.CTkProgressBar(master=menuFrame, orientation="horizontal")
    progressbar.pack(fill="x")

    etcDirectory = os.path.join(rootDirectory, "etc")
    filesToSearch = [("passwd", [etcDirectory]), ("shadow", [etcDirectory]), ("sudoers", [etcDirectory]), ("group", [etcDirectory])]

    extracted_data_dir = os.path.join(mainFolder, "User Account Data")
    os.makedirs(extracted_data_dir, exist_ok=True)

    total_files = len(filesToSearch)
    files_not_found = []
    for i, (fileToSearch, directories) in enumerate(filesToSearch):
        for filePath in fileCrawler(rootDirectory, directories, fileToSearch):
            with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                with open(os.path.join(extracted_data_dir, fileToSearch), "w", encoding='utf-8') as output:
                    for line in input:
                        output.write(line)
            break  
        else:
            files_not_found.append(fileToSearch)

    progress = (i + 1) / total_files * 100
    progressbar.set(progress)

    if not files_not_found:
        appendReport("<h3>User Account Data</h3>")
        appendReport("Data extraction was successful. Extracted data is located at " + extracted_data_dir)
    elif len(files_not_found) < len(filesToSearch):
        appendReport("<h3>User Account Data</h3>")
        appendReport("Data extraction was partially successful. Some files were not found. Extracted data is located at " + extracted_data_dir)
    else:
        appendReport("<h3>User Account Data</h3>")
        appendReport("Data extraction failed. No files were found.")
    
    checkExtractionStatus(stat, extracted_data_dir)
    progressbar.destroy()

    return