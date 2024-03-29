#####################################################################
# Imports and setups
#####################################################################

import os
import tempfile
import fnmatch
import chardet
import tkinter.messagebox as messagebox
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

def fileExtractAll(directory):
    for folderName, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(folderName, filename)

#####################################################################
# Report
#####################################################################

def generateReport(osi, host, timez):

    reportPath = os.path.join(mainFolder, "LinXtrac Report.html")
    with open(reportPath, "w") as reportFile:

        reportFile.write("<html>\n")
        reportFile.write("<head>\n")
        reportFile.write("<title>LinXtrac - Linux Extraction System Report</title>\n")
        reportFile.write("<style>\n")
        reportFile.write("body { font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4; }\n")
        reportFile.write("h1, h2, h3, h4 { color: #333; }\n")
        reportFile.write("h1 { border-bottom: 2px solid #333; padding-bottom: 10px; }\n")
        reportFile.write("h2 { color: #666; }\n")
        reportFile.write("h3 { margin-top: 20px; }\n")
        reportFile.write("p, li { line-height: 1.6; }\n")
        reportFile.write("ul { padding-left: 20px; }\n")
        reportFile.write("ul li { margin-bottom: 10px; }\n")
        reportFile.write("details { background-color: #fff; padding: 10px; margin-bottom: 10px; border-radius: 5px; box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1); }\n")
        reportFile.write("summary { cursor: pointer; }\n")
        reportFile.write("</style>\n")
        reportFile.write("</head>\n")
        reportFile.write("<body>\n")
        
        reportFile.write("<h1>LinXtrac</h1>\n")
        reportFile.write("<h2>Linux Extraction System Report</h2>\n")
        
        reportFile.write("<h3>OS Information</h3>\n")
        reportFile.write("<details>\n")
        reportFile.write("<summary>Click to view details</summary>\n")
        reportFile.write("<p><b>OS Version:</b><br> {}<br><b>Host:</b><br> {}<br><b>Time:</b><br> {}</p>\n".format(osi, host, timez))
        reportFile.write("</details>\n")

    return

def appendReport(data):

    reportPath = os.path.join(mainFolder, "LinXtrac Report.html")
    with open(reportPath, "a") as reportFile:
        reportFile.write("{}\n".format(data))
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

def getUserAccountInfo(stat):

    stat.configure(text="Extracting...")

    etcDirectory = os.path.join(rootDirectory, "etc")
    filesToSearch = [("passwd", [etcDirectory]), ("shadow", [etcDirectory]), ("sudoers", [etcDirectory]), ("group", [etcDirectory])]

    extracted_data_dir = os.path.join(mainFolder, "User Account Data")
    os.makedirs(extracted_data_dir, exist_ok=True)

    total_files = len(filesToSearch)
    files_not_found = []
    permission_denied_files = [] 
    for i, (fileToSearch, directories) in enumerate(filesToSearch):
        for filePath in fileCrawler(rootDirectory, directories, fileToSearch):
            try:
                with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                    with open(os.path.join(extracted_data_dir, fileToSearch), "w", encoding='utf-8') as output:
                        for line in input:
                            output.write(line)
                break  
            except PermissionError:
                permission_denied_files.append(filePath) 
                continue
        else:
            files_not_found.append(fileToSearch)

    appendReport("<h3>User Account Data</h3>")
    if not files_not_found:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    elif len(files_not_found) < len(filesToSearch):
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    else:
        appendReport("<details><summary>Data extraction failed. No files were found. Click to view details.</summary>")
    
    checkExtractionStatus(stat, extracted_data_dir)

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if files_not_found:
        appendReport("<h4>Files Not Found or Partially Present</h4>")
        appendReport("<p>The following files were not found or were only partially present:</p>")
        appendReport("<ul>")
        for file in files_not_found:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    appendReport("</details>")
    return

#####################################################################
# System and Application Logs
#####################################################################

def getLogs(stat):

    stat.configure(text="Extracting...")

    logDirectory = os.path.join(rootDirectory, "var", "log")
    filesToSearch = [(file, [logDirectory]) for file in os.listdir(logDirectory)]

    extracted_data_dir = os.path.join(mainFolder, "System and Application Logs")
    os.makedirs(extracted_data_dir, exist_ok=True)

    total_files = len(filesToSearch)
    files_not_found = []
    permission_denied_files = [] 
    for i, (fileToSearch, directories) in enumerate(filesToSearch):
        for filePath in fileCrawler(rootDirectory, directories, fileToSearch):
            try:
                with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                    with open(os.path.join(extracted_data_dir, fileToSearch), "w", encoding='utf-8') as output:
                        for line in input:
                            output.write(line)
            except PermissionError:
                permission_denied_files.append(filePath) 
                continue
            break  
        else:
            files_not_found.append(fileToSearch)

    appendReport("<h3>System and Application Logs</h3>")
    if not files_not_found:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    elif len(files_not_found) < len(filesToSearch):
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    else:
        appendReport("<details><summary>Data extraction failed. No files were found. Click to view details.</summary>")
    
    checkExtractionStatus(stat, extracted_data_dir)

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if files_not_found:
        appendReport("<h4>Files Not Found or Partially Present</h4>")
        appendReport("<p>The following files were not found or were only partially present:</p>")
        appendReport("<ul>")
        for file in files_not_found:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    appendReport("</details>")
    return

#####################################################################
# Web Browsing Activity
#####################################################################

def getBrowserData(stat):
    stat.configure(text="Extracting...")
    
    base_directories = ['.config/google-chrome', '.mozilla/Firefox', '.config/Opera', '.cache']

    extracted_data_dir = os.path.join(mainFolder, "Web Browsing Activity")
    os.makedirs(extracted_data_dir, exist_ok=True)

    permission_denied_files = []  
    not_found_directories = []  
    total_directories = 0

    for username in os.listdir(os.path.join(rootDirectory, 'home')):
        for base_dir in base_directories:
            total_directories += 1
            directory = os.path.join(rootDirectory, 'home', username, base_dir)
            if os.path.exists(directory):
                for filePath in fileExtractAll(directory):
                    try:
                        with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                            with open(os.path.join(extracted_data_dir, os.path.basename(filePath)), "w", encoding='utf-8') as output:
                                for line in input:
                                    output.write(line)
                    except PermissionError:
                        permission_denied_files.append(filePath)  
                        continue
                    except IsADirectoryError:
                        continue
                    except FileNotFoundError:
                        not_found_directories.append(directory)  
                        continue
            else:
                not_found_directories.append(directory)

    appendReport("<h3>Web Browsing Activity</h3>")
    if not not_found_directories:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    elif len(not_found_directories) < total_directories:
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    else:
        appendReport("<details><summary>Data extraction failed. No files were found.</summary>")

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if not_found_directories:
        appendReport("<h4>Files Not Found or Partially Present</h4>")
        appendReport("<p>The following files were not found or were only partially present:</p>")
        appendReport("<ul>")
        for directory in not_found_directories:
            appendReport(f"<li>{directory}</li>")
        appendReport("</ul>")
    appendReport("</details>")

    checkExtractionStatus(stat, extracted_data_dir)

    return

#####################################################################
# System Files
#####################################################################

def getSystemFiles(stat):
    stat.configure(text="Extracting...")

    directoriesToSearch = ["/etc/*-release", "/etc/hostname", "/etc/hosts", "/var/lib/networkmanager", "/var/lib/dhclient", "/var/lib/dhcp"]

    extracted_data_dir = os.path.join(mainFolder, "System Files")
    os.makedirs(extracted_data_dir, exist_ok=True)

    permission_denied_files = []  
    not_found_files = []  
    empty_files = []  

    for directory in directoriesToSearch:
        directory = os.path.join(rootDirectory, directory.lstrip('/'))  
        directory_path, directory_name = os.path.split(directory)
        if any(dir_entry.name.lower() == directory_name.lower() for dir_entry in os.scandir(directory_path)):
            for filePath in fileExtractAll(directory):
                try:
                    with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                        if input.read().strip() == "":
                            empty_files.append(filePath)
                            continue
                        with open(os.path.join(extracted_data_dir, os.path.basename(filePath.lower())), "w", encoding='utf-8') as output:
                            for line in input:
                                output.write(line)
                except PermissionError:
                    permission_denied_files.append(filePath)  
                    continue
                except FileNotFoundError:
                    not_found_files.append(filePath) 
                    continue
        else:
            not_found_files.append(directory)

    appendReport("<h3>System Files</h3>")
    if not not_found_files and not empty_files:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    elif len(not_found_files) < len(directoriesToSearch) or empty_files:
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found or were empty. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    else:
        appendReport("<details><summary>Data extraction failed. No files were found.</summary>")

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if not_found_files:
        appendReport("<h4>Files Not Found</h4>")
        appendReport("<p>The following files were not found:</p>")
        appendReport("<ul>")
        for file in not_found_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if empty_files:
        appendReport("<h4>Empty Files</h4>")
        appendReport("<p>The following files were empty:</p>")
        appendReport("<ul>")
        for file in empty_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    appendReport("</details>")

    checkExtractionStatus(stat, extracted_data_dir)

    return

#####################################################################
# Bash History
#####################################################################

def getBashHistory(stat):

    stat.configure(text="Extracting...")

    bashHistoryFile = ".bash_history"
    homeDirectory = os.path.join(rootDirectory, "home")
    directoriesToSearch = [os.path.join(homeDirectory, username) for username in os.listdir(homeDirectory)]

    extracted_data_dir = os.path.join(mainFolder, "Bash History")
    os.makedirs(extracted_data_dir, exist_ok=True)

    files_not_found = []
    permission_denied_files = [] 
    for directory in directoriesToSearch:
        for filePath in fileCrawler(rootDirectory, [directory], bashHistoryFile):
            try:
                with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                    with open(os.path.join(extracted_data_dir, os.path.basename(directory) + "_" + bashHistoryFile), "w", encoding='utf-8') as output:
                        for line in input:
                            output.write(line)
                break  
            except PermissionError:
                permission_denied_files.append(filePath) 
                continue
        else:
            files_not_found.append(directory)

    appendReport("<h3>Bash History</h3>")
    if not files_not_found:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    elif len(files_not_found) < len(directoriesToSearch):
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    else:
        appendReport("<details><summary>Data extraction failed. No files were found. Click to view details.</summary>")
    
    checkExtractionStatus(stat, extracted_data_dir)

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if files_not_found:
        appendReport("<h4>Directories Not Found or Partially Present</h4>")
        appendReport("<p>The following directories were not found or were only partially present:</p>")
        appendReport("<ul>")
        for directory in files_not_found:
            appendReport(f"<li>{directory}</li>")
        appendReport("</ul>")

    appendReport("</details>")

    return

#####################################################################
# Trash
#####################################################################

def getTrash(stat):
    stat.configure(text="Extracting...")

    trashDirectory = ".local/share/Trash"
    homeDirectory = os.path.join(rootDirectory, "home")
    directoriesToSearch = [os.path.join(homeDirectory, username, trashDirectory) for username in os.listdir(homeDirectory)]

    extracted_data_dir = os.path.join(mainFolder, "Trash")
    os.makedirs(extracted_data_dir, exist_ok=True)

    directories_not_found = []
    permission_denied_files = [] 
    for directory in directoriesToSearch:
        if os.path.exists(directory):
            for filePath in fileExtractAll(directory):
                try:
                    with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                        with open(os.path.join(extracted_data_dir, os.path.basename(directory) + "_" + os.path.basename(filePath)), "w", encoding='utf-8') as output:
                            for line in input:
                                output.write(line)
                except PermissionError:
                    permission_denied_files.append(filePath) 
                    continue
        else:
            directories_not_found.append(directory)

    appendReport("<h3>Trash Data</h3>")
    if not directories_not_found and not permission_denied_files:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    elif len(directories_not_found) < len(directoriesToSearch):
        appendReport("<details><summary>Data extraction was partially successful. Some directories were not found. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    else:
        appendReport("<details><summary>Data extraction failed. No directories were found. Click to view details.</summary>")
    
    checkExtractionStatus(stat, extracted_data_dir)

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if directories_not_found:
        appendReport("<h4>Directories Not Found or Partially Present</h4>")
        appendReport("<p>The following directories were not found or were only partially present:</p>")
        appendReport("<ul>")
        for directory in directories_not_found:
            appendReport(f"<li>{directory}</li>")
        appendReport("</ul>")

    appendReport("</details>")

    return

#####################################################################
# Recent Files
#####################################################################

def getRecentFiles(stat):

    stat.configure(text="Extracting...")

    extracted_data_dir = os.path.join(mainFolder, "Recent Files")
    os.makedirs(extracted_data_dir, exist_ok=True)

    permission_denied_files = []  
    not_found_files = []  

    for username in os.listdir(os.path.join(rootDirectory, 'home')):
        filePath = os.path.join(rootDirectory, 'home', username, '.local/share/recently-used.xbel')
        if os.path.exists(filePath):
            try:
                with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                    with open(os.path.join(extracted_data_dir, f"{username}_recently-used.xbel"), "w", encoding='utf-8') as output:
                        for line in input:
                            output.write(line)
            except PermissionError:
                permission_denied_files.append(filePath)  
                continue
        else:
            not_found_files.append(filePath)

    appendReport("<h3>Recent Files</h3>")
    if not not_found_files and not permission_denied_files:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    elif len(not_found_files) < len(os.listdir(os.path.join(rootDirectory, 'home'))):
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    else:
        appendReport("<details><summary>Data extraction failed. No files were found. Click to view details.</summary>")

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if not_found_files:
        appendReport("<h4>Files Not Found</h4>")
        appendReport("<p>The following files were not found:</p>")
        appendReport("<ul>")
        for file in not_found_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    appendReport("</details>")

    checkExtractionStatus(stat, extracted_data_dir)

    return

#####################################################################
# Startup Items
#####################################################################

def getStartup(stat):
    stat.configure(text="Extracting...")

    directoriesToSearch = ["/etc/systemd/system", "/usr/lib/systemd/system"]
    initDirectories = fnmatch.filter(os.listdir(os.path.join(rootDirectory, 'etc')), 'init*')
    directoriesToSearch.extend(os.path.join('/etc', dir) for dir in initDirectories)

    extracted_data_dir = os.path.join(mainFolder, "Startup Items")
    os.makedirs(extracted_data_dir, exist_ok=True)

    permission_denied_files = []  
    not_found_files = []  

    for directory in directoriesToSearch:
        directory = os.path.join(rootDirectory, directory.lstrip('/'))  
        directory_path, directory_name = os.path.split(directory)
        if any(dir_entry.name.lower() == directory_name.lower() for dir_entry in os.scandir(directory_path)):
            for filePath in fileExtractAll(directory):
                try:
                    with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                        with open(os.path.join(extracted_data_dir, os.path.basename(filePath.lower())), "w", encoding='utf-8') as output:
                            for line in input:
                                output.write(line)
                except PermissionError:
                    permission_denied_files.append(filePath)  
                    continue
                except FileNotFoundError:
                    not_found_files.append(filePath) 
                    continue
        else:
            not_found_files.append(directory)

    appendReport("<h3>Startup Items</h3>")
    if not not_found_files and not permission_denied_files:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    elif len(not_found_files) < len(directoriesToSearch):
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    else:
        appendReport("<details><summary>Data extraction failed. No files were found. Click to view details.</summary>")

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if not_found_files:
        appendReport("<h4>Files Not Found</h4>")
        appendReport("<p>The following files were not found:</p>")
        appendReport("<ul>")
        for file in not_found_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    appendReport("</details>")

    checkExtractionStatus(stat, extracted_data_dir)

    return

#####################################################################
# Scheduled Tasks
#####################################################################

def getScheduledTasks(stat):

    stat.configure(text="Extracting...")

    directoriesToSearch = ["/var/spool/crontabs", "/var/spool/atjobs", "/etc/anacron"]
    cronDirectories = fnmatch.filter(os.listdir(os.path.join(rootDirectory, 'etc')), 'cron*')
    directoriesToSearch.extend(os.path.join('/etc', dir) for dir in cronDirectories)

    extracted_data_dir = os.path.join(mainFolder, "Scheduled Tasks")
    os.makedirs(extracted_data_dir, exist_ok=True)

    permission_denied_files = []  
    not_found_files = []  

    for directory in directoriesToSearch:
        directory = os.path.join(rootDirectory, directory.lstrip('/'))  
        directory_path, directory_name = os.path.split(directory)
        if any(dir_entry.name.lower() == directory_name.lower() for dir_entry in os.scandir(directory_path)):
            for filePath in fileExtractAll(directory):
                try:
                    with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                        with open(os.path.join(extracted_data_dir, os.path.basename(filePath.lower())), "w", encoding='utf-8') as output:
                            for line in input:
                                output.write(line)
                except PermissionError:
                    permission_denied_files.append(filePath)  
                    continue
                except FileNotFoundError:
                    not_found_files.append(filePath) 
                    continue
        else:
            not_found_files.append(directory)

    appendReport("<h3>Scheduled Tasks</h3>")
    if not not_found_files and not permission_denied_files:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    elif len(not_found_files) < len(directoriesToSearch):
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found. Click to view details.</summary><br>Extracted data is located at " + extracted_data_dir)
    else:
        appendReport("<details><summary>Data extraction failed. No files were found. Click to view details.</summary>")

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if not_found_files:
        appendReport("<h4>Files Not Found</h4>")
        appendReport("<p>The following files were not found:</p>")
        appendReport("<ul>")
        for file in not_found_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    appendReport("</details>")

    checkExtractionStatus(stat, extracted_data_dir)

    return

#####################################################################
# SSH Files
#####################################################################

def getSSHFiles(stat):
    stat.configure(text="Extracting...")

    ssh_files = ["authorized_keys", "known_hosts", "config", "id_*"]
    users = os.listdir(os.path.join(rootDirectory, 'home'))

    extracted_data_dir = os.path.join(mainFolder, "SSH Files")
    os.makedirs(extracted_data_dir, exist_ok=True)

    files_not_found = []
    permission_denied_files = [] 

    for user in users:
        files_to_search = [(file, [os.path.join('home', user, '.ssh')]) for file in ssh_files]
        for i, (file_to_search, directories) in enumerate(files_to_search):
            for filePath in fileCrawler(rootDirectory, directories, file_to_search):
                try:
                    with open(filePath, "r", encoding='utf-8', errors='ignore') as input:
                        with open(os.path.join(extracted_data_dir, f"{user}_{file_to_search}"), "w", encoding='utf-8') as output:
                            for line in input:
                                output.write(line)
                except PermissionError:
                    permission_denied_files.append(filePath) 
                    continue
                break  
            else:
                files_not_found.append(file_to_search)

    appendReport("<h3>SSH Files</h3>")
    if not files_not_found:
        appendReport("<details><summary>Data extraction was successful. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    elif len(files_not_found) < len(files_to_search):
        appendReport("<details><summary>Data extraction was partially successful. Some files were not found. Click to view details.</summary>")
        appendReport("<p>Extracted data is located at " + extracted_data_dir + "</p>")
    else:
        appendReport("<details><summary>Data extraction failed. No files were found. Click to view details.</summary>")
    
    checkExtractionStatus(stat, extracted_data_dir)

    if permission_denied_files:
        appendReport("<h4>Files with Denied Permissions</h4>")
        appendReport("<p>The following files could not be accessed due to permission restrictions:</p>")
        appendReport("<ul>")
        for file in permission_denied_files:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    if files_not_found:
        appendReport("<h4>Files Not Found or Partially Present</h4>")
        appendReport("<p>The following files were not found or were only partially present:</p>")
        appendReport("<ul>")
        for file in files_not_found:
            appendReport(f"<li>{file}</li>")
        appendReport("</ul>")

    appendReport("</details>")
    return

#####################################################################
# Keyword Searching
#####################################################################

def searchKeyword(keyword):
    
    matching_files = []
    matching_dirs = []
    skipped_files = []

    for root, dirs, files in os.walk(mainFolder):
        for dir in dirs:
            if keyword in dir:
                matching_dirs.append(os.path.join(root, dir))
        for file in files:
            if keyword in file:
                matching_files.append(os.path.join(root, file))
            else:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        rawdata = f.read()
                        result = chardet.detect(rawdata)
                        encoding = result['encoding']
                        if encoding is None:
                            encoding = 'utf-8' 
                        try:
                            text = rawdata.decode(encoding)
                            if keyword in text:
                                matching_files.append(file_path)
                        except UnicodeDecodeError:
                            skipped_files.append(file_path)
                except Exception as e:
                    print(f"Error reading file {file}: {e}")

    appendReport(f"<h3>Search for keyword '{keyword}'</h3>")
    if matching_files or matching_dirs:
        messagebox.showinfo("Search Results", f"Keyword '{keyword}' found.\nFirst 3 matches:\n\n" +
                            '\n'.join(matching_files[:3] + matching_dirs[:3]) +
                            "\n\nCheck report for more details.")
        appendReport("<details><summary>Click to view details.</summary>")
        appendReport("<p>Found in the following files:</p>")
        appendReport("<ul>")
        for file_path in matching_files:
            appendReport(f"<li>{file_path}</li>")
        appendReport("</ul>")
        if skipped_files:
            appendReport("<p>Some files could not be decoded:</p>")
            appendReport("<ul>")
            for file_path in skipped_files:
                appendReport(f"<li>{file_path}</li>")
            appendReport("</ul>")
        appendReport("</details>")
    else:
        messagebox.showinfo("Search Results", f"No matches found for keyword '{keyword}'. Check report for details.")
        appendReport("<details><summary>No matches found for keyword '{keyword}'. Click to view details.</summary>")
        appendReport("<p>No files or directories found containing the keyword.</p>")
        appendReport("</details>")

    return matching_files, matching_dirs

#####################################################################
# END
#####################################################################