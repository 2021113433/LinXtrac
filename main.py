#####################################################################
# Imports and setups
#####################################################################

import customtkinter
import threading
from extension import *

#####################################################################
# Startup
#####################################################################

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("800x600")
app.resizable(False, False)
app.title("LinXtrac - Linux Extraction System")

###

mainFrame = customtkinter.CTkFrame(master=app)
mainFrame.pack(pady=20, padx=60, fill="both", expand=True)

title = customtkinter.CTkLabel(master=mainFrame, text="\n\n\nLinXtrac", font=("Helvetica", 30))
title.pack()
subTitle = customtkinter.CTkLabel(master=mainFrame, text="\nLinux Extraction System", font=("Helvetica", 20))
subTitle.pack()
flavourText = customtkinter.CTkLabel(master=mainFrame, text="Discover the power of efficient forensic investigation with LinXtrac", font=("Helvetica", 16, "italic"))
flavourText.pack()
 
###

subFrame = customtkinter.CTkFrame(master=mainFrame)
subFrame.pack(padx=80, pady=80)

directoryText = customtkinter.CTkLabel(master=subFrame, text="No directory chosen", font=("Helvetica", 13))
directoryText.grid(row=0, column=1, padx=10)
directoryButton = customtkinter.CTkButton(master=subFrame, text="Choose Directory", command=lambda: [getDirectory(),getInfo(), mainFrame.pack_forget(), menuFrame.pack(pady=20, padx=60, fill="both", expand=True)])
directoryButton.grid(row=0, column=0, padx=10, pady=10)

###

exitFrame = customtkinter.CTkFrame(master=mainFrame)
exitFrame.pack(padx=1, pady=5, side="right")
exitButton = customtkinter.CTkButton(master=exitFrame, text="Exit", command=app.destroy)
exitButton.pack(padx=10, pady=10)

#####################################################################
# Menu
#####################################################################

menuFrame = customtkinter.CTkFrame(master=app)

title = customtkinter.CTkLabel(master=menuFrame, text="\nLinXtrac", font=("Helvetica", 30))
title.pack()
subTitle = customtkinter.CTkLabel(master=menuFrame, text="Linux Extraction System", font=("Helvetica", 20))
subTitle.pack(padx=10, pady=10)

###

searchFrame = customtkinter.CTkFrame(master=menuFrame)
searchFrame.pack()

searchLabel = customtkinter.CTkLabel(master=searchFrame, text="Keyword Search: ")
searchLabel.pack(side="left", padx=10, pady=10)
searchEntry = customtkinter.CTkEntry(master=searchFrame)
searchEntry.pack(side="left", padx=10, pady=10)
searchButton = customtkinter.CTkButton(master=searchFrame, text="Search", command=lambda: searchKeyword(searchEntry.get()))
searchButton.pack(side="left", padx=10, pady=10)

###

ButtonFrame = customtkinter.CTkFrame(master=menuFrame)
ButtonFrame.pack(padx=30, pady=30)

UADStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
UADStatus.grid(row=0, column=1, padx=10)
UADButton = customtkinter.CTkButton(master=ButtonFrame,text="User Account Details",command=lambda: threading.Thread(target=getUserAccountInfo, args=(UADStatus,)).start())
UADButton.grid(row=0, column=0, padx=10, pady=10) 

logStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
logStatus.grid(row=1, column=1, padx=10)
logButton = customtkinter.CTkButton(master=ButtonFrame,text="Sys & App Logs",command=lambda: threading.Thread(target=getLogs, args=(logStatus,)).start())
logButton.grid(row=1, column=0, padx=10, pady=10) 

browStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
browStatus.grid(row=2, column=1, padx=10)
browButton = customtkinter.CTkButton(master=ButtonFrame,text="Web Browsing Activity",command=lambda: threading.Thread(target=getBrowserData, args=(browStatus,)).start())
browButton.grid(row=2, column=0, padx=10, pady=10) 

sysStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
sysStatus.grid(row=3, column=1, padx=10)
sysButton = customtkinter.CTkButton(master=ButtonFrame,text="System Files",command=lambda: threading.Thread(target=getSystemFiles, args=(sysStatus,)).start())
sysButton.grid(row=3, column=0, padx=10, pady=10) 

bashStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
bashStatus.grid(row=4, column=1, padx=10)
bashButton = customtkinter.CTkButton(master=ButtonFrame,text="Bash History",command=lambda: threading.Thread(target=getBashHistory, args=(bashStatus,)).start())
bashButton.grid(row=4, column=0, padx=10, pady=10) 

trashStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
trashStatus.grid(row=0, column=3, padx=10)
trashButton = customtkinter.CTkButton(master=ButtonFrame,text="Trash",command=lambda: threading.Thread(target=getTrash, args=(trashStatus,)).start())
trashButton.grid(row=0, column=2, padx=10, pady=10) 

recentStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
recentStatus.grid(row=1, column=3, padx=10)
recentButton = customtkinter.CTkButton(master=ButtonFrame,text="Recent Files",command=lambda: threading.Thread(target=getRecentFiles, args=(recentStatus,)).start())
recentButton.grid(row=1, column=2, padx=10, pady=10) 

startStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
startStatus.grid(row=2, column=3, padx=10)
startButton = customtkinter.CTkButton(master=ButtonFrame,text="Startup Items",command=lambda: threading.Thread(target=getStartup, args=(startStatus,)).start())
startButton.grid(row=2, column=2, padx=10, pady=10) 

scheStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
scheStatus.grid(row=3, column=3, padx=10)
scheButton = customtkinter.CTkButton(master=ButtonFrame,text="Scheduled Tasks",command=lambda: threading.Thread(target=getScheduledTasks, args=(scheStatus,)).start())
scheButton.grid(row=3, column=2, padx=10, pady=10) 

sshStatus = customtkinter.CTkLabel(master=ButtonFrame, text="Not Extracted")
sshStatus.grid(row=4, column=3, padx=10)
sshButton = customtkinter.CTkButton(master=ButtonFrame,text="SSH Files",command=lambda: threading.Thread(target=getSSHFiles, args=(sshStatus,)).start())
sshButton.grid(row=4, column=2, padx=10, pady=10) 

###

exitFrame = customtkinter.CTkFrame(master=menuFrame)
exitFrame.pack(padx=1, pady=5, side="right")
exitButton = customtkinter.CTkButton(master=exitFrame, text="Exit", command=lambda: [closeReport(), app.destroy()])
exitButton.pack(padx=10, pady=10)

app.mainloop()

#####################################################################
# END
#####################################################################